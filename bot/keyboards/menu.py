from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

MAGIC_NUMBER_CALLBACK = "menu:get_magic_number"
FATE_CALLBACK = "menu:get_fate"
SETTINGS_CALLBACK = "menu:settings"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔢 Найти моё число", callback_data=MAGIC_NUMBER_CALLBACK)],
            [InlineKeyboardButton(text="📜 Моя судьба", callback_data=FATE_CALLBACK)],
            [InlineKeyboardButton(text="⚙️ Настройки", callback_data=SETTINGS_CALLBACK)],
        ]
    )
