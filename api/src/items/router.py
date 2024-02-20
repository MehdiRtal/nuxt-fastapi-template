from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from src.db import DBSession
from src.auth.dependencies import require_superuser

from src.items.models import Item, ItemCreate, ItemRead, ItemUpdate
from src.items.exceptions import ItemNotFound, ItemAlreadyExists


router = APIRouter(tags=["Items"], prefix="/items")

@router.get("/")
async def get_items(db: DBSession, limit: int = 100, offset: int = 0) -> list[ItemRead]:
    statement = select(Item).offset(offset).limit(limit)
    db_items = await db.exec(statement)
    db_items = db_items.all()
    if not db_items:
        raise ItemNotFound()
    return db_items

@router.get("/{item_id}")
async def get_item(db: DBSession, item_id: int):
    db_item = await db.get(Item, item_id)
    if not db_item:
        raise ItemNotFound()
    return db_item

@router.post("/", status_code=201, dependencies=[Depends(require_superuser)])
async def add_item(db: DBSession, item: ItemCreate) -> ItemRead:
    try:
        db_item = Item(**item.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
    except IntegrityError:
        raise ItemAlreadyExists()
    return db_item

@router.patch("/{item_id}", dependencies=[Depends(require_superuser)])
async def update_item(db: DBSession, item_id: int, item: ItemUpdate) -> ItemRead:
    db_item = await db.get(Item, item_id)
    if not db_item:
        raise ItemNotFound()
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", dependencies=[Depends(require_superuser)])
async def delete_item(db: DBSession, item_id: int) -> ItemRead:
    db_item = await db.get(Item, item_id)
    if not db_item:
        raise ItemNotFound()
    db.delete(db_item)
    await db.commit()
    return db_item
