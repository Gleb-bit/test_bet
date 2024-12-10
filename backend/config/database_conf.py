from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config.settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, future=True)


async def get_session():
    async with SessionLocal() as session:
        yield session
