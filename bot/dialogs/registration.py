from __future__ import annotations

import logging
from datetime import datetime

from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from bot.dialogs.states import Registration
from bot.keyboards.menu import main_menu_keyboard
from bot.lexicon import texts
from bot.services.magic import calculate_magic_number
from db.orm import FateData, ORMController, UserAlreadyExistsError

logger = logging.getLogger(__name__)


async def on_start(start_data, dialog_manager: DialogManager):
    event = dialog_manager.event
    if isinstance(event, Message):
        await event.answer(texts.START_MESSAGE)
    await dialog_manager.switch_to(Registration.full_name)


def registration_dialog() -> Dialog:
    return Dialog(
        Window(
            Const(texts.ASK_FULL_NAME),
            MessageInput(on_full_name_received),
            state=Registration.full_name,
        ),
        Window(
            Const(texts.ASK_BIRTH_DATE),
            MessageInput(on_birth_date_received),
            state=Registration.birth_date,
        ),
        on_start=on_start,
    )


async def on_full_name_received(
    message: Message, _: MessageInput, dialog_manager: DialogManager, **__
):
    full_name = (message.text or message.html_text or "").strip()
    if not full_name:
        await message.answer(texts.ASK_FULL_NAME)
        return
    dialog_manager.dialog_data["full_name"] = full_name
    logger.info("User %s provided full name", message.from_user.id if message.from_user else "unknown")
    await dialog_manager.switch_to(Registration.birth_date)


async def on_birth_date_received(
    message: Message, _: MessageInput, dialog_manager: DialogManager, **kwargs
):
    if message.from_user is None:
        return
    try:
        birth_date = datetime.strptime((message.text or "").strip(), "%d.%m.%Y").date()
    except (ValueError, AttributeError):
        await message.answer(texts.INVALID_DATE)
        return
    telegram_id = message.from_user.id
    magic_number = calculate_magic_number(birth_date)

    orm: ORMController = dialog_manager.middleware_data["orm"]
    fate: FateData | None = await orm.get_fate_by_magic_number(magic_number)
    fate_id = fate.id if fate else None

    try:
        await orm.add_user(
            telegram_id=telegram_id,
            full_name=dialog_manager.dialog_data["full_name"],
            birth_date=birth_date,
            magic_number=magic_number,
            fate_id=fate_id,
        )
        logger.info("Registered new user %s", telegram_id)
    except UserAlreadyExistsError:
        user = await orm.get_user(telegram_id)
        if user is not None:
            await orm.update_user(
                user,
                full_name=dialog_manager.dialog_data["full_name"],
                birth_date=birth_date,
                magic_number=magic_number,
                fate_id=fate_id,
            )
            logger.info("Updated existing user %s", telegram_id)
    await message.answer(texts.REGISTRATION_COMPLETE)
    await message.answer(texts.MENU_PROMPT, reply_markup=main_menu_keyboard())
    await dialog_manager.done()


