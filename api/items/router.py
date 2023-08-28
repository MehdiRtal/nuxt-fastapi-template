from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi_restful.cbv import cbv
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from database import Database
from auth.dependencies import require_superuser

from .models import Item, ItemCreate, ItemRead, ItemUpdate


router = APIRouter(tags=["Items"], prefix="/items", dependencies=[Depends(require_superuser)])

@cbv(router)
class Items:
    db: Database

    @router.get("/")
    async def get_items(self, limit: int = 100, offset: int = 0) -> list[ItemRead]:
        statement = select(Item).offset(offset).limit(limit)
        db_items = await self.db.exec(statement)
        db_items = db_items.all()
        if not db_items:
            raise HTTPException(404, "No items found")
        return db_items

    @router.get("/{item_id}")
    async def get_item(self, item_id: int):
        db_item = await self.db.get(Item, item_id)
        if not db_item:
            raise HTTPException(404, "Item not found")
        return db_item

    @router.post("/", status_code=201)
    async def add_item(self, item: ItemCreate) -> ItemRead:
        try:
            db_item = Item(**item.model_dump())
            self.db.add(db_item)
            await self.db.commit()
            await self.db.refresh(db_item)
        except IntegrityError:
            raise HTTPException(400, "Item already exists")
        return db_item

    @router.patch("/{item_id}")
    async def update_item(self, item_id: int, item: ItemUpdate) -> ItemRead:
        db_item = await self.db.get(Item, item_id)
        if not db_item:
            raise HTTPException(404, "Item not found")
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    @router.delete("/{item_id}")
    async def delete_item(self, item_id: int) -> ItemRead:
        db_item = await self.db.get(Item, item_id)
        if not db_item:
            raise HTTPException(404, "Item not found")
        self.db.delete(db_item)
        await self.db.commit()
        return db_item