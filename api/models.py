from sqlmodel import Field, SQLModel
from pydantic import ConfigDict, EmailStr, constr
import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default).decode()

class BaseModel(SQLModel):
    model_config = ConfigDict(json_loads=orjson.loads, json_dumps=orjson_dumps)


class DefaultResponse(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: int | None = Field(None, primary_key=True)
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
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(None, regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    balance: int | None = None
    is_verified: bool | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None