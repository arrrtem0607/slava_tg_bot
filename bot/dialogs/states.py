from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    start = State()
    full_name = State()
    birth_date = State()
