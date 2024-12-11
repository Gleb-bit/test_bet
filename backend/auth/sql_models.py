from typing import Optional

from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship


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
