from sqlmodel import Field, AutoString
from pydantic import EmailStr

from api.models import BaseModel


class UserBase(BaseModel):
    full_name: str
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)

class User(UserBase, table=True):
    id: int | None = Field(None, primary_key=True)
    password: str
    balance: float = Field(0.0)
    is_verified: bool = Field(False)
    is_active: bool = Field(True)
    is_superuser: bool = Field(False)
    google_oauth_refresh_token: str | None = Field(None)

class UserCreate(UserBase):
    password: str = Field(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

class UserRead(UserBase):
    id: int
    balance: float
    is_verified: bool
    is_superuser: bool
    is_active: bool

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(None, regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    balance: float | None = None
    is_verified: bool | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    google_oauth_refresh_token: str | None = None
