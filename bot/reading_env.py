from __future__ import annotations

from dataclasses import dataclass

from environs import Env


def _init_env() -> Env:
    env = Env()
    env.read_env()
    return env


@dataclass(frozen=True)
class BotConfig:
    token: str


@dataclass(frozen=True)
class DatabaseConfig:
    url: str


@dataclass(frozen=True)
class Settings:
    bot: BotConfig
    db: DatabaseConfig


def load_settings() -> Settings:
    env = _init_env()
    return Settings(
        bot=BotConfig(token=env.str("BOT_TOKEN")),
        db=DatabaseConfig(url=env.str("DATABASE_URL")),
    )
