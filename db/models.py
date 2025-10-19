from __future__ import annotations

from datetime import datetime, date

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Fate(Base):
    __tablename__ = "fates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    magic_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="fate")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("telegram_id", name="uq_users_telegram_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    magic_number: Mapped[int] = mapped_column(Integer, nullable=False)
    fate_id: Mapped[int | None] = mapped_column(ForeignKey("fates.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    fate: Mapped[Fate | None] = relationship(back_populates="users")
