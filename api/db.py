from fastapi import Depends
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated

from config import settings


engine = create_async_engine(str(settings.DB_URL))

async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_db_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db_session)]
