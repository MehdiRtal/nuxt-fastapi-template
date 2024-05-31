from fastapi import Depends
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from sqlalchemy.orm import sessionmaker


from src.config import settings


postgres_engine = create_async_engine(str(settings.POSTGRES_URL))

PostgresSessionLocal = sessionmaker(bind=postgres_engine, class_=AsyncSession, expire_on_commit=False)

async def init_postgres():
    async with postgres_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_postgres_session():
    async with PostgresSessionLocal() as session:
        yield session

PostgresSession = Annotated[AsyncSession, Depends(get_postgres_session)]
