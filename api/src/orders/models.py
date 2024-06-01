from sqlmodel import Field

from src.models import BaseModel

from src.orders.constants import OrderStatus


class OrderBasePublic(BaseModel):
    pass

class OrderBase(OrderBasePublic):
    user_id: int = Field(foreign_key="user.id")
    price: float = Field()
    status: OrderStatus = Field(OrderStatus.PENDING)

class Order(OrderBase, table=True):
    id: int | None = Field(None, primary_key=True)

class OrderRead(OrderBase):
    id: int

class OrderCreatePublic(OrderBasePublic):
    pass

class OrderCreate(OrderBase):
    pass

class OrderUpdatePublic(BaseModel):
    pass

class OrderUpdate(OrderUpdatePublic):
    user_id: int | None = None
    price: float | None = None
    status: OrderStatus | None = None
