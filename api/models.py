from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import EmailStr, constr
import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default).decode()

class BaseModel(SQLModel):
    status: str = "success"
    message: Optional[str] = None

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    password: str
    balance: int = Field(0)
    is_verified: bool = Field(False)
    is_superuser: bool = Field(False)
    is_active: bool = Field(True)

class UserCreate(UserBase):
    password: constr(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

class UserRead(UserBase):
    id: int
    balance: int
    is_verified: bool
    is_superuser: bool
    is_active: bool

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    balance: Optional[int] = None
    is_verified: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_active: Optional[bool] = None