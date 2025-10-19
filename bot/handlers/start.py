from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.dialogs.states import Registration

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(Registration.start, mode=StartMode.RESET_STACK)
