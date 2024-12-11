from datetime import datetime
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from auth.sql_models import User
from models.sql.events import Event


class UserBet(SQLModel, table=True):
    """Модель пользователя"""

    __table_args__ = (UniqueConstraint("user_id", "event_id", name="user_bet"),)

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="user_bets")

    event_id: int | None = Field(default=None, foreign_key="event.id")
    event: Event | None = Relationship(back_populates="event_bets")

    created_at: datetime | None = Field(default=datetime.now)
