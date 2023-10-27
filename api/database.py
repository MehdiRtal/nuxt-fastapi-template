from fastapi import Depends
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Annotated

from config import settings


engine = AsyncEngine(create_engine(settings.DATABASE_URL))

async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def get_db_session():
    Session = sessionmaker(bind=engine, class_=AsyncSession)
    async with Session() as session:
        yield session

Database = Annotated[AsyncSession, Depends(get_db_session)]
