import enum
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from models.sql.events import Event


class User(SQLModel, table=True):
    """Модель пользователя"""

    __table_args__ = (UniqueConstraint("email"),)

    id: Optional[int] = Field(default=None, primary_key=True)

    email: EmailStr = Field(index=True, nullable=False)
    hashed_password: str = Field(nullable=False)

    first_name: str = Field(nullable=False)
    last_name: Optional[str] = Field(default=None)

    is_active: bool = Field(default=True)

    user_bets: list["UserBet"] = Relationship(back_populates="user")


class BetStatus(enum.Enum):
    """Статус ставки"""

    Not_started = "Not_started"
    Win = "Win"
    Lose = "Lose"


class UserBet(SQLModel, table=True):
    """Модель пользователя"""

    __table_args__ = (UniqueConstraint("user_id", "event_id", name="user_bet"),)

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int | None = Field(foreign_key="user.id", nullable=False)
    user: User | None = Relationship(back_populates="user_bets")

    event_id: int | None = Field(foreign_key="event.id", nullable=False)
    event: Event | None = Relationship()

    bet_amount: float = Field(nullable=False)
    created_at: datetime | None = Field(default_factory=datetime.now)
    status: BetStatus | None = Field(default=BetStatus.Not_started)
