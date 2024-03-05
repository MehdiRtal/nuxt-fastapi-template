from fastapi import Depends
from typing import Annotated

from src.db import DBSession

from src.items.repository import ItemsRepository
from src.items.service import ItemsService


def get_items_service_session(db: DBSession):
    items_repository = ItemsRepository(db)
    items_service = ItemsService(items_repository)
    return items_service

ItemsServiceSession = Annotated[ItemsService, Depends(get_items_service_session)]
