from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.keyboards.menu import (
    FATE_CALLBACK,
    MAGIC_NUMBER_CALLBACK,
    SETTINGS_CALLBACK,
    main_menu_keyboard,
)
from bot.lexicon import texts
from db.orm import ORMController

router = Router()


@router.message(Command("menu"))
async def show_main_menu(message: Message) -> None:
    await message.answer(texts.MENU_PROMPT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == MAGIC_NUMBER_CALLBACK)
async def handle_magic_number(callback: CallbackQuery, orm: ORMController) -> None:
    await callback.answer()
    if callback.from_user is None or callback.message is None:
        return
    user = await orm.get_user(callback.from_user.id)
    if user is None:
        await callback.message.answer(texts.USER_NOT_REGISTERED)
        return
    await callback.message.answer(
        texts.MAGIC_NUMBER_MESSAGE.format(magic_number=user.magic_number)
    )


@router.callback_query(F.data == FATE_CALLBACK)
async def handle_fate(callback: CallbackQuery, orm: ORMController) -> None:
    await callback.answer()
    if callback.from_user is None or callback.message is None:
        return
    user = await orm.get_user(callback.from_user.id)
    if user is None:
        await callback.message.answer(texts.USER_NOT_REGISTERED)
        return
    fate_text = texts.FATE_NOT_FOUND
    if user.fate_id is not None:
        fate = await orm.get_fate_by_magic_number(user.magic_number)
        if fate is not None:
            fate_text = texts.FATE_MESSAGE.format(description=fate.description)
    await callback.message.answer(fate_text)


@router.callback_query(F.data == SETTINGS_CALLBACK)
async def handle_settings(callback: CallbackQuery) -> None:
    await callback.answer("Скоро здесь появятся настройки!", show_alert=True)
