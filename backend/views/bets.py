from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from config.database_conf import get_session
from core.sqlalchemy.crud import Crud
from models.bets import Bet, BetCreate

bets_router = APIRouter()
bet_crud = Crud(Bet)


@bets_router.get("/", response_model=List[Bet])
async def list_bets(
    session: AsyncSession = Depends(get_session),
):
    return await bet_crud.list(session)


@bets_router.get("/{bet_id}", response_model=Bet)
async def retrieve_bet(bet_id: int, session: AsyncSession = Depends(get_session)):
    return await bet_crud.retrieve(bet_id, session)


@bets_router.post("/", response_model=Bet)
async def create_bet(bet: BetCreate, session: AsyncSession = Depends(get_session)):
    return await bet_crud.create(bet, session)
