from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from src.db import DBSession

from src.items.models import Item, ItemCreate, ItemRead, ItemUpdate
from src.items.exceptions import ItemNotFound, ItemAlreadyExists


class ItemsService:
    def __init__(self, db: DBSession):
        self.db = db

    async def get_items(self, limit: int, offset: int) -> list[ItemRead]:
        statement = select(Item).offset(offset).limit(limit)
        db_items = await self.db.exec(statement)
        db_items = db_items.all()
        if not db_items:
            raise ItemNotFound()
        return db_items

    async def get_item(self, item_id: int) -> ItemRead:
        db_item = await self.db.get(Item, item_id)
        if not db_item:
            raise ItemNotFound()
        return db_item

    async def add_item(self, item: ItemCreate) -> ItemRead:
        try:
            db_item = Item(**item.model_dump())
            self.db.add(db_item)
            await self.db.commit()
            await self.db.refresh(db_item)
        except IntegrityError:
            raise ItemAlreadyExists()
        return db_item

    async def update_item(self, item_id: int, item: ItemUpdate) -> ItemRead:
        db_item = await self.db.get(Item, item_id)
        if not db_item:
            raise ItemNotFound()
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def delete_item(self, item_id: int) -> ItemRead:
        db_item = await self.db.get(Item, item_id)
        if not db_item:
            raise ItemNotFound()
        self.db.delete(db_item)
        await self.db.commit()
        return db_item
