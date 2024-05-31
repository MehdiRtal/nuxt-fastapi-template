from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import Type, TypeVar, Generic

from src.postgres import AsyncSession
from src.models import BaseModel


T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, postgres: AsyncSession, model: Type[T]):
        self.postgres = postgres
        self.model = model

    async def get(self, limit: int, offset: int):
        statement = select(self.model).offset(offset).limit(limit)
        db_entity = await self.postgres.exec(statement)
        db_entity = db_entity.all()
        return db_entity

    async def get_by_id(self, entity_id: int):
        db_entity = await self.postgres.get(self.model, entity_id)
        return db_entity

    async def add(self, entity: T, extra_data: dict | None = None, refresh: bool = True):
        try:
            db_entity = self.model.model_validate(entity, update=extra_data)
            self.postgres.add(db_entity)
            await self.postgres.commit()
            if refresh:
                await self.postgres.refresh(db_entity)
        except IntegrityError:
            await self.postgres.rollback()
            return None
        return db_entity

    async def update(self, instance: object, refresh: bool = True) -> T:
        self.postgres.add(instance)
        await self.postgres.commit()
        if refresh:
            await self.postgres.refresh(instance)
        return instance

    async def update_by_id(self, entity_id: int, entity: T, extra_data: dict | None = None, refresh: bool = True):
        db_entity = await self.get_by_id(entity_id)
        if not db_entity:
            return None
        entity_data = entity.model_dump(exclude_unset=True)
        db_entity.sqlmodel_update(entity_data, update=extra_data)
        self.postgres.add(db_entity)
        await self.postgres.commit()
        if refresh:
            await self.postgres.refresh(db_entity)
        return db_entity


    async def delete_by_id(self, entity_id: int):
        db_entity = await self.get_by_id(entity_id)
        if not db_entity:
            return None
        await self.postgres.delete(db_entity)
        await self.postgres.commit()
        return db_entity
