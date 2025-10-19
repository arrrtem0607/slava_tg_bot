from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from bot.dialogs.states import Registration
from bot.keyboards.menu import (
    FATE_CALLBACK,
    MAGIC_NUMBER_CALLBACK,
    SETTINGS_CALLBACK,
    main_menu_keyboard,
)
from bot.lexicon import texts

router = Router()


@router.message(Command("menu"))
async def show_main_menu(message: Message) -> None:
    await message.answer(texts.MENU_PROMPT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == MAGIC_NUMBER_CALLBACK)
async def handle_magic_number(callback: CallbackQuery, dialog_manager: DialogManager) -> None:
    await callback.answer()
    await dialog_manager.switch_to(Registration.magic_number)


@router.callback_query(F.data == FATE_CALLBACK)
async def handle_fate(callback: CallbackQuery, dialog_manager: DialogManager) -> None:
    await callback.answer()
    await dialog_manager.switch_to(Registration.fate)


@router.callback_query(F.data == SETTINGS_CALLBACK)
async def handle_settings(callback: CallbackQuery) -> None:
    await callback.answer("Скоро здесь появятся настройки!", show_alert=True)
