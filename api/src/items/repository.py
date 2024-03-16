from sqlmodel import select

from src.repository import BaseRepository
from src.postgres import AsyncSession

from src.items.models import Item
from src.items.exceptions import ItemNotFound


class ItemsRepository(BaseRepository[Item]):
    def __init__(self, postgres: AsyncSession):
        super().__init__(postgres, Item)

    async def get_by_user_id(self, user_id: int, limit: int, offset: int):
        statement = select(Item).where(Item.user_id == user_id).offset(offset).limit(limit)
        db_items = await self.postgres.exec(statement)
        db_items = db_items.all()
        if not db_items:
            raise ItemNotFound
        return db_items

    async def get_by_id_by_user_id(self, user_id: int, item_id: int):
        statement = select(Item).where(Item.user_id == user_id).where(Item.id == item_id)
        db_item = await self.postgres.exec(statement)
        db_item = db_item.first()
        if not db_item:
            raise ItemNotFound
        return db_item

    async def update_by_id_by_user_id(self, user_id: int, item_id: int, item: Item, refresh: bool = True):
        db_item = self.get_by_id_by_user_id(user_id, item_id)
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        await self.postgres.add(db_item)
        await self.postgres.commit()
        if refresh:
            await self.postgres.refresh(db_item)
        return db_item

    async def delete_by_id_by_user_id(self, user_id: int, item_id: int):
        db_item = self.get_by_id_by_user_id(user_id, item_id)
        await self.postgres.delete(db_item)
        await self.postgres.commit()
        return db_item
