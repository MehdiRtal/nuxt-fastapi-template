from sqlmodel import Field

from src.models import BaseModel


class ItemBase(BaseModel):
    user_id: int = Field(foreign_key="user.id")
    name: str = Field()

class Item(ItemBase, table=True):
    id: int | None = Field(None, primary_key=True)

class ItemRead(ItemBase):
    id: int

class ItemCreate(ItemBase):
    user_id: int | None = None

class ItemUpdate(BaseModel):
    user_id: int | None = None
    name: str | None = None
