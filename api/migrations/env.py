from alembic import context
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine
import asyncio

from config import settings
from models import *


target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    context.configure(url=settings.POSTGRES_URL, target_metadata=target_metadata,)
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    engine = AsyncEngine(create_engine(settings.POSTGRES_URL))
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())