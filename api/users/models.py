from sqlmodel import Field, AutoString
from pydantic import EmailStr

from models import BaseModel


class UserBase(BaseModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)

class User(UserBase, table=True):
    id: int | None = Field(None, primary_key=True)
    password: str
    is_verified: bool = Field(False)
    is_active: bool = Field(True)
    is_superuser: bool = Field(False)

class UserCreate(UserBase):
    password: str = Field(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

class UserRead(UserBase):
    id: int
    is_verified: bool
    is_superuser: bool
    is_active: bool

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(None, regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    is_verified: bool | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
