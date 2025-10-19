from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from bot.dialogs.registration import registration_dialog
from bot.handlers.start import router as start_router
from bot.reading_env import load_settings
from bot.services.middlewares import DatabaseSessionMiddleware


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = load_settings()

    bot = Bot(token=settings.bot.token, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)
    dp.include_router(registration_dialog())
    dp.update.outer_middleware(DatabaseSessionMiddleware())
    setup_dialogs(dp)

    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
