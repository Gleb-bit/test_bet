from datetime import datetime

from pydantic import BaseModel


class EventNumber(BaseModel):
    number: str


class MakeBet(BaseModel):
    event_number: str
    bet_amount: float


class MakeBetReturn(BaseModel):
    event: EventNumber

    class Config:
        from_attributes = True


class BetRead(BaseModel):
    event: EventNumber
    bet_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
