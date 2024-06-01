from sqlmodel import Field, AutoString
from pydantic import EmailStr, ConfigDict

from src.models import BaseModel


class UserBasePublic(BaseModel):
    full_name: str
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)

class UserBase(UserBasePublic):
    password: str = Field()
    is_verified: bool = Field(False)
    is_active: bool = Field(True)
    is_superuser: bool = Field(False)
    google_oauth_refresh_token: str | None = Field(None)
    apple_oauth_refresh_token: str | None = Field(None)

class User(UserBase, table=True):
    id: int | None = Field(None, primary_key=True)

class UserCreatePublic(UserBasePublic):
    model_config = ConfigDict(regex_engine="python-re")

    password: str = Field(schema_extra={"pattern": r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"})

class UserCreate(UserBase):
    pass

class UserReadPublic(UserBasePublic):
    id: int
    is_verified: bool
    is_active: bool
    is_superuser: bool

class UserRead(UserBase):
    id: int

class UserUpdatePublic(BaseModel):
    full_name: str | None = None

class UserUpdate(BaseModel):
    model_config = ConfigDict(regex_engine="python-re")

    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(None, schema_extra={"pattern": r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"})
    is_verified: bool | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    google_oauth_refresh_token: str | None = None
    apple_oauth_refresh_token: str | None = None
