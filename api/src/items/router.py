from fastapi import APIRouter, Depends

from src.db import DBSession
from src.auth.dependencies import require_superuser

from src.items.models import ItemCreate, ItemRead, ItemUpdate
from src.items.service import ItemsService


router = APIRouter(tags=["Items"], prefix="/items")

@router.get("/")
async def get_items(db: DBSession, limit: int = 100, offset: int = 0) -> list[ItemRead]:
    items_service = ItemsService(db)
    return await items_service.get_items(limit, offset)

@router.get("/{item_id}")
async def get_item(db: DBSession, item_id: int):
    items_service = ItemsService(db)
    return await items_service.get_item(item_id)

@router.post("/", status_code=201, dependencies=[Depends(require_superuser)])
async def add_item(db: DBSession, item: ItemCreate) -> ItemRead:
    items_service = ItemsService(db)
    return await items_service.add_item(item)

@router.patch("/{item_id}", dependencies=[Depends(require_superuser)])
async def update_item(db: DBSession, item_id: int, item: ItemUpdate) -> ItemRead:
    items_service = ItemsService(db)
    return await items_service.update_item(item_id, item)

@router.delete("/{item_id}", dependencies=[Depends(require_superuser)])
async def delete_item(db: DBSession, item_id: int) -> ItemRead:
    items_service = ItemsService(db)
    return await items_service.delete_item(item_id)
