from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.conf import AUTH_MODEL, auth
from auth.sql_models import User, UserBet
from config.database_conf import get_session
from core.sqlalchemy.crud import Crud
from core.sqlalchemy.orm import Orm
from models.pydantic.user_bets import MakeBet, MakeBetReturn, BetRead
from models.sql.events import Event

bet_crud = Crud(UserBet)
bet_router = APIRouter()


@bet_router.post("/bet", response_model=MakeBetReturn)
async def post_bet(
    user_bet: MakeBet,
    credentials: AUTH_MODEL = Depends(auth.get_request_user),
    session: AsyncSession = Depends(get_session),
):
    user = await Orm.scalar(User, session, User.email == credentials.email)
    event = await Orm.scalar(Event, session, Event.number == user_bet.event_number)
    if not event:
        raise HTTPException(400, "Event not found")

    bet_data = {
        "user_id": user.id,
        "event_id": event.id,
        "bet_amount": user_bet.bet_amount,
    }

    return await bet_crud.create(bet_data, session, UserBet.event)


@bet_router.get("/bets", response_model=List[BetRead])
async def list_bets(
    credentials: AUTH_MODEL = Depends(auth.get_request_user),
    session: AsyncSession = Depends(get_session),
):
    user = await Orm.scalar(User, session, User.email == credentials.email)
    user_bets = await bet_crud.list(session, UserBet.event, UserBet.user_id == user.id)

    return user_bets
