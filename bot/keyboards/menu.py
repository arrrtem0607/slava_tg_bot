from __future__ import annotations

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Row

from bot.dialogs.states import Registration


async def magic_number_clicked(callback: CallbackQuery, _: Button, manager: DialogManager):
    await callback.answer()
    await manager.switch_to(Registration.magic_number)


async def fate_clicked(callback: CallbackQuery, _: Button, manager: DialogManager):
    await callback.answer()
    await manager.switch_to(Registration.fate)


main_menu_row = Row(
    Button(text="🔢 Найти моё число", id="find_magic_number", on_click=magic_number_clicked),
    Button(text="📜 Моя судьба", id="show_fate", on_click=fate_clicked),
)
