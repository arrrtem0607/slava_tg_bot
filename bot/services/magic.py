from __future__ import annotations

from datetime import date


def calculate_magic_number(birth_date: date) -> int:
    digits = [int(char) for char in birth_date.strftime("%d%m%Y")]
    return sum(digits)
