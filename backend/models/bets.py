import enum
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, model_validator
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field


class EventStatus(enum.Enum):
    """Статус события"""

    Unfinished = "Unfinished"
    First_win = "First_win"
    Second_win = "Second_win"


class Bet(SQLModel, table=True):
    """Модель ставки"""

    __table_args__ = (UniqueConstraint("number"),)

    id: Optional[int] = Field(default=None, primary_key=True)

    number: str = Field()
    coefficient: Decimal = Field(gt=0, max_digits=5, decimal_places=2)

    deadline: int = Field(gt=0)
    status: EventStatus


class BetCreate(BaseModel):
    number: str
    coefficient: Decimal = Field(gt=0, max_digits=5, decimal_places=2)

    deadline: int = Field(gt=0)
    status: EventStatus

    @model_validator(mode="before")
    def check_coefficient(cls, values):
        coefficient = values["coefficient"]
        if not isinstance(coefficient, float):
            raise ValueError(
                "coefficient must be a float value with 2 values after point"
            )

        return values
