from fastapi import Depends
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated

from src.config import settings


engine = create_async_engine(str(settings.POSTGRES_URL))

async def init_postgres():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_postgres_session():
    async with AsyncSession(engine) as session:
        yield session

PostgresSession = Annotated[AsyncSession, Depends(get_postgres_session)]
