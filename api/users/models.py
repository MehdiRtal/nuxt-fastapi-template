from sqlmodel import Field
from pydantic import EmailStr, constr
from models import BaseModel


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