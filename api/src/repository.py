from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import Type, TypeVar, Generic

from src.postgres import AsyncSession
from src.models import BaseModel
from src.exceptions import EntityNotFound, EntityAlreadyExists


T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, postgres: AsyncSession, model: Type[T]):
        self.postgres = postgres
        self.model = model

    async def get(self, limit: int, offset: int):
        statement = select(self.model).offset(offset).limit(limit)
        db_entity = await self.postgres.exec(statement)
        db_entity = db_entity.all()
        if not db_entity:
            raise EntityNotFound
        return db_entity

    async def get_by_id(self, entity_id: int):
        db_entity = await self.postgres.get(self.model, entity_id)
        if not db_entity:
            raise EntityNotFound
        return db_entity

    async def add(self, entity: T, refresh: bool = True):
        try:
            db_entity = self.model(**entity.model_dump())
            self.postgres.add(db_entity)
            await self.postgres.commit()
            if refresh:
                await self.postgres.refresh(db_entity)
        except IntegrityError:
            self.postgres.rollback()
            raise EntityAlreadyExists
        return db_entity

    async def update(self, instance: object, refresh: bool = True) -> T:
        self.postgres.add(instance)
        await self.postgres.commit()
        if refresh:
            await self.postgres.refresh(instance)
        return instance

    async def update_by_id(self, entity_id: int, entity: T, refresh: bool = True):
        db_entity = self.get_by_id(entity_id)
        for key, value in entity.model_dump(exclude_unset=True).items():
            setattr(db_entity, key, value)
        self.postgres.add(db_entity)
        await self.postgres.commit()
        if refresh:
            await self.postgres.refresh(db_entity)
        return db_entity

    async def delete_by_id(self, entity_id: int):
        db_entity = self.get_by_id(entity_id)
        self.postgres.delete(db_entity)
        await self.postgres.commit()
        return db_entity
