from sqlmodel import Field

from src.models import BaseModel


class ItemBase(BaseModel):
    user_id: int | None = Field(None, foreign_key="user.id")

class Item(ItemBase, table=True):
    id: int | None = Field(None, primary_key=True)

class ItemRead(ItemBase):
    id: int

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    user_id: int | None = None
