from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.conf import AUTH_MODEL, auth
from config.database_conf import get_session
from core.sqlalchemy.crud import Crud
from models.pydantic.events import EventCreate
from models.sql.events import Event

events_router = APIRouter()
event_crud = Crud(Event)


@events_router.get("/", response_model=List[Event])
async def list_events(
    session: AsyncSession = Depends(get_session),
):
    return await event_crud.list(session)


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
