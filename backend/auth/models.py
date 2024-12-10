from typing import Optional

from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: Optional[str] = None


class UserReadModel(BaseModel):
    id: int
    email: EmailStr


class TokenModel(BaseModel):
    email: EmailStr
