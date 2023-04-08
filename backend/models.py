from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import EmailStr, constr
import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

class BaseModel(SQLModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserBase(BaseModel):
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    balance: int = Field(default=0)
    is_verified: bool = Field(default=False)

class UserCreate(UserBase):
    password: constr(regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

class UserRead(UserBase):
    id: int
    balance: int
    is_verified: bool

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, regex="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    balance: Optional[int] = None
    is_verified: Optional[bool] = None


class OderBase(BaseModel):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    quantity: int
    target: str

class Order(OderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: str = Field(default="pending")

class OrderRead(OderBase):
    id: int

class OrderCreate(OderBase):
    pass

class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    target: Optional[str] = None


class ProductBase(BaseModel):
    name: str
    price: int
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductRead(ProductBase):
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    category_id: Optional[int] = None


class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class CategoryRead(CategoryBase):
    id: int

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None


class AccountBase(BaseModel):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    credentials: str

class Account(AccountBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class AccountRead(AccountBase):
    id: int

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    user_id: Optional[int] = None
    category_id: Optional[int] = None
    credentials: Optional[str] = None


class Token(BaseModel):
    token: str