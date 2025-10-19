"""Пакет с обработчиками команд и колбэков."""

from .menu import router as menu_router
from .start import router as start_router

__all__ = ["start_router", "menu_router"]
