from __future__ import annotations

import logging
from datetime import datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.states import Registration
from bot.keyboards.menu import main_menu_row
from bot.lexicon import texts
from bot.services.magic import calculate_magic_number
from db.orm import ORMController, UserAlreadyExistsError

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
        Window(
            Const(texts.MENU_PROMPT),
            main_menu_row,
            Button(Const("⚙️ Настройки"), id="settings_placeholder", on_click=settings_placeholder),
            state=Registration.menu,
        ),
        Window(
            Format(texts.MAGIC_NUMBER_MESSAGE),
            Button(Const("⬅️ Назад"), id="back_from_magic", on_click=back_to_menu),
            state=Registration.magic_number,
            getter=get_magic_number,
        ),
        Window(
            Format("{fate_text}"),
            Button(Const("⬅️ Назад"), id="back_from_fate", on_click=back_to_menu),
            state=Registration.fate,
            getter=get_fate_text,
        ),
        on_start=on_start,
    )


async def on_full_name_received(message: Message, dialog_manager: DialogManager, **__):
    full_name = (message.text or message.html_text or "").strip()
    if not full_name:
        await message.answer(texts.ASK_FULL_NAME)
        return
    dialog_manager.dialog_data["full_name"] = full_name
    logger.info("User %s provided full name", message.from_user.id if message.from_user else "unknown")
    await dialog_manager.switch_to(Registration.birth_date)


async def on_birth_date_received(message: Message, dialog_manager: DialogManager, **kwargs):
    if message.from_user is None:
        return
    try:
        birth_date = datetime.strptime((message.text or "").strip(), "%d.%m.%Y").date()
    except (ValueError, AttributeError):
        await message.answer(texts.INVALID_DATE)
        return
    telegram_id = message.from_user.id
    dialog_manager.dialog_data["telegram_id"] = telegram_id
    dialog_manager.dialog_data["birth_date"] = birth_date
    magic_number = calculate_magic_number(birth_date)
    dialog_manager.dialog_data["magic_number"] = magic_number

    orm: ORMController = dialog_manager.middleware_data["orm"]
    fate = await orm.get_fate_by_magic_number(magic_number)
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
    dialog_manager.dialog_data["fate"] = fate.description if fate else None

    await message.answer(texts.REGISTRATION_COMPLETE)
    await dialog_manager.switch_to(Registration.menu)


async def get_magic_number(dialog_manager: DialogManager, **__):
    magic_number = dialog_manager.dialog_data.get("magic_number")
    if magic_number is None:
        telegram_id = dialog_manager.dialog_data.get("telegram_id")
        orm: ORMController | None = dialog_manager.middleware_data.get("orm")
        if telegram_id and orm:
            user = await orm.get_user(telegram_id)
            if user is not None:
                magic_number = user.magic_number
                dialog_manager.dialog_data["magic_number"] = magic_number
    if magic_number is None:
        magic_number = "-"
    return {"magic_number": magic_number}


async def get_fate_text(dialog_manager: DialogManager, **__):
    fate_text = dialog_manager.dialog_data.get("fate")
    if fate_text is None:
        telegram_id = dialog_manager.dialog_data.get("telegram_id")
        orm: ORMController | None = dialog_manager.middleware_data.get("orm")
        if telegram_id and orm:
            user = await orm.get_user(telegram_id)
            if user and user.fate:
                fate_text = user.fate.description
                dialog_manager.dialog_data["fate"] = fate_text
    if not fate_text:
        fate_text = texts.FATE_NOT_FOUND
    else:
        fate_text = texts.FATE_MESSAGE.format(description=fate_text)
    return {"fate_text": fate_text}


async def back_to_menu(callback: CallbackQuery, _: Button, manager: DialogManager):
    await callback.answer()
    await manager.switch_to(Registration.menu)


async def settings_placeholder(callback: CallbackQuery, _: Button, manager: DialogManager):
    await callback.answer("Скоро здесь появятся настройки!", show_alert=True)
