from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import Type, TypeVar, Generic

from src.db import AsyncSession
from src.models import BaseModel
from src.exceptions import EntityNotFound, EntityAlreadyExists


T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def get(self, limit: int, offset: int):
        statement = select(self.model).offset(offset).limit(limit)
        db_entity = await self.db.exec(statement)
        db_entity = db_entity.all()
        if not db_entity:
            raise EntityNotFound()
        return db_entity

    async def get_by_id(self, entity_id: int):
        db_entity = await self.db.get(self.model, entity_id)
        if not db_entity:
            raise EntityNotFound()
        return db_entity

    async def add(self, entity: T, refresh: bool = True):
        try:
            db_entity = self.model(**entity.model_dump())
            self.db.add(db_entity)
            await self.db.commit()
            if refresh:
                await self.db.refresh(db_entity)
        except IntegrityError:
            raise EntityAlreadyExists()
        return db_entity

    async def update(self, instance: object, refresh: bool = True) -> T:
        self.db.add(instance)
        await self.db.commit()
        if refresh:
            await self.db.refresh(instance)
        return instance

    async def update_by_id(self, entity_id: int, entity: T, refresh: bool = True):
        db_entity = self.get_by_id(entity_id)
        for key, value in entity.model_dump(exclude_unset=True).items():
            setattr(db_entity, key, value)
        self.db.add(db_entity)
        await self.db.commit()
        if refresh:
            await self.db.refresh(db_entity)
        return db_entity

    async def delete_by_id(self, entity_id: int):
        db_entity = self.get_by_id(entity_id)
        self.db.delete(db_entity)
        await self.db.commit()
        return db_entity
