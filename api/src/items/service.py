from src.exceptions import EntityNotFound, EntityAlreadyExists

from src.items.models import Item
from src.items.exceptions import ItemNotFound, ItemAlreadyExists
from src.items.repository import ItemsRepository


class ItemsService:
    def __init__(self, items_repository: ItemsRepository):
        self.items_repository = items_repository

    async def get_items(self, limit: int, offset: int):
        try:
            db_items = await self.items_repository.get(limit, offset)
        except EntityNotFound:
            raise ItemNotFound
        return db_items

    async def get_item(self, item_id: int):
        try:
            db_item = await self.items_repository.get_by_id(item_id)
        except EntityNotFound:
            raise ItemNotFound
        return db_item
    async def add_item(self, item: Item):
        try:
            db_item = await self.items_repository.add(item)
        except EntityAlreadyExists:
            raise ItemAlreadyExists
        return db_item

    async def update_item(self, item_id: int, item: Item):
        try:
            db_items = await self.items_repository.update_by_id(item_id, item)
        except EntityNotFound:
            raise ItemNotFound
        return db_items

    async def delete_item(self, item_id: int):
        try:
            db_items = await self.items_repository.delete_by_id(item_id)
        except EntityNotFound:
            raise ItemNotFound
        return db_items
