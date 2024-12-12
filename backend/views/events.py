from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.conf import AUTH_MODEL, auth
from auth.sql_models import UserBet, BetStatus
from config.database_conf import get_session
from core.sqlalchemy.crud import Crud
from core.sqlalchemy.orm import Orm
from models.pydantic.events import EventCreate, EventPatch
from models.sql.events import Event, EventStatus

events_router = APIRouter()
event_crud = Crud(Event)


@events_router.get("/", response_model=List[Event])
async def list_events(
    session: AsyncSession = Depends(get_session),
):
    return await event_crud.list(
        session, filters=[Event.deadline > datetime.now().timestamp()]
    )


@events_router.get("/{event_id}", response_model=Event)
async def retrieve_event(event_id: int, session: AsyncSession = Depends(get_session)):
    return await event_crud.retrieve(event_id, session)


@events_router.post("/", response_model=Event)
async def post_event(
    event: EventCreate,
    session: AsyncSession = Depends(get_session),
    credentials: AUTH_MODEL = Depends(auth.get_request_user),
):
    return await event_crud.create(event, session)


@events_router.patch("/{event_id}", response_model=Event)
async def patch_event(
    event_id: int,
    event_data: EventPatch,
    session: AsyncSession = Depends(get_session),
    credentials: AUTH_MODEL = Depends(auth.get_request_user),
):
    updated_event = await event_crud.update(
        event_data.model_dump(exclude_unset=True), event_id, session
    )

    event_bets = (
        (await Orm.where(UserBet, UserBet.event_id == event_id, session))
        .scalars()
        .all()
    )

    for bet in event_bets:
        status = (
            BetStatus.Win
            if updated_event.status == EventStatus.First_win
            else BetStatus.Lose
        )
        await Orm.update_field(
            UserBet, {"status": status}, session, UserBet.id == bet.id
        )

    return await event_crud.retrieve(event_id, session)
