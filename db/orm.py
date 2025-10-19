from __future__ import annotations

from datetime import date
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Fate, User


class UserAlreadyExistsError(Exception):
    """Raised when trying to register a user that already exists."""


@dataclass(slots=True, frozen=True)
class FateData:
    id: int
    description: str


class ORMController:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_user(
        self,
        telegram_id: int,
        full_name: str,
        birth_date: date,
        magic_number: int,
        fate_id: int | None = None,
    ) -> User:
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            birth_date=birth_date,
            magic_number=magic_number,
            fate_id=fate_id,
        )
        self._session.add(user)
        try:
            await self._session.commit()
        except IntegrityError as exc:  # pragma: no cover - depends on database state
            await self._session.rollback()
            raise UserAlreadyExistsError from exc
        await self._session.refresh(user)
        return user

    async def update_user(
        self,
        user: User,
        *,
        full_name: str | None = None,
        birth_date: date | None = None,
        magic_number: int | None = None,
        fate_id: int | None = None,
    ) -> User:
        if full_name is not None:
            user.full_name = full_name
        if birth_date is not None:
            user.birth_date = birth_date
        if magic_number is not None:
            user.magic_number = magic_number
        user.fate_id = fate_id
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get_user(self, telegram_id: int) -> User | None:
        result = await self._session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()

    async def get_fate_by_magic_number(self, number: int) -> FateData | None:
        result = await self._session.execute(
            select(Fate.id, Fate.description).where(Fate.magic_number == number)
        )
        row = result.first()
        if row is None:
            return None
        return FateData(id=row.id, description=row.description)

    async def update_fate(self, number: int, description: str) -> Fate:
        stmt = (
            update(Fate)
            .where(Fate.magic_number == number)
            .values(description=description)
            .returning(Fate)
        )
        result = await self._session.execute(stmt)
        fate = result.fetchone()
        if fate is None:
            fate = Fate(magic_number=number, description=description)
            self._session.add(fate)
            await self._session.commit()
            await self._session.refresh(fate)
            return fate
        await self._session.commit()
        return fate[0] if isinstance(fate, tuple) else fate

    async def link_user_fate(self, user: User, fate: Fate | None) -> User:
        user.fate_id = fate.id if fate else None
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def flush(self) -> None:
        await self._session.flush()

    async def close(self) -> None:
        await self._session.close()

    async def __aenter__(self) -> "ORMController":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self._session.close()
