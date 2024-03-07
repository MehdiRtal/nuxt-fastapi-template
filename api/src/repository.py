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
        postgres_entity = await self.postgres.exec(statement)
        postgres_entity = postgres_entity.all()
        if not postgres_entity:
            raise EntityNotFound()
        return postgres_entity

    async def get_by_id(self, entity_id: int):
        postgres_entity = await self.postgres.get(self.model, entity_id)
        if not postgres_entity:
            raise EntityNotFound()
        return postgres_entity

    async def add(self, entity: T, refresh: bool = True):
        try:
            postgres_entity = self.model(**entity.model_dump())
            self.postgres.add(postgres_entity)
            await self.postgres.commit()
            if refresh:
                await self.postgres.refresh(postgres_entity)
        except IntegrityError:
            raise EntityAlreadyExists()
        return postgres_entity

    async def update(self, instance: object, refresh: bool = True) -> T:
        self.postgres.add(instance)
        await self.postgres.commit()
        if refresh:
            await self.postgres.refresh(instance)
        return instance

    async def update_by_id(self, entity_id: int, entity: T, refresh: bool = True):
        postgres_entity = self.get_by_id(entity_id)
        for key, value in entity.model_dump(exclude_unset=True).items():
            setattr(postgres_entity, key, value)
        self.postgres.add(postgres_entity)
        await self.postgres.commit()
        if refresh:
            await self.postgres.refresh(postgres_entity)
        return postgres_entity

    async def delete_by_id(self, entity_id: int):
        postgres_entity = self.get_by_id(entity_id)
        self.postgres.delete(postgres_entity)
        await self.postgres.commit()
        return postgres_entity
