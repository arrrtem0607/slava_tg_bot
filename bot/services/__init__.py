"""Служебные функции бота."""

from .magic import calculate_magic_number
from .middlewares import DatabaseSessionMiddleware

__all__ = ["calculate_magic_number", "DatabaseSessionMiddleware"]
