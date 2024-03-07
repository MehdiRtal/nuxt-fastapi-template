from fastapi import Depends
from typing import Annotated

from src.postgres import PostgresSession

from src.items.repository import ItemsRepository
from src.items.service import ItemsService


def get_items_service_session(postgres: PostgresSession):
    items_repository = ItemsRepository(postgres)
    items_service = ItemsService(items_repository)
    return items_service

ItemsServiceSession = Annotated[ItemsService, Depends(get_items_service_session)]
