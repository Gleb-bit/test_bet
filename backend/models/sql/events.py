import enum
from decimal import Decimal
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field


class EventStatus(enum.Enum):
    """Статус события"""

    Unfinished = "Unfinished"
    First_win = "First_win"
    Second_win = "Second_win"


class Event(SQLModel, table=True):
    """Модель события"""

    __table_args__ = (UniqueConstraint("number"),)

    id: Optional[int] = Field(default=None, primary_key=True)

    number: str = Field()
    coefficient: Decimal = Field(gt=0, max_digits=5, decimal_places=2)

    deadline: int = Field(gt=0)
    status: EventStatus
