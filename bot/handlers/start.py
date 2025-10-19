from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.dialogs.states import Registration
from bot.keyboards.menu import main_menu_keyboard
from bot.lexicon import texts
from db.orm import ORMController

router = Router()


@router.message(CommandStart())
async def command_start(
    message: Message, dialog_manager: DialogManager, orm: ORMController
) -> None:
    if message.from_user is not None:
        user = await orm.get_user(message.from_user.id)
        if user is not None:
            await message.answer(
                texts.WELCOME_BACK,
                reply_markup=main_menu_keyboard(),
            )
            return
    await dialog_manager.start(Registration.start, mode=StartMode.RESET_STACK)
