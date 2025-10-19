"""TODO: реализовать сервис для обработки платежей."""

from __future__ import annotations

from typing import Any


async def create_payment(*args: Any, **kwargs: Any) -> None:  # pragma: no cover - заглушка
    """Создание платежа будет реализовано в будущем."""
    raise NotImplementedError("Платёжный функционал ещё не готов")


async def check_payment_status(payment_id: str) -> None:  # pragma: no cover - заглушка
    """Проверка статуса платежа будет реализована позже."""
    raise NotImplementedError("Платёжный функционал ещё не готов")
