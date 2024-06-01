from sqlmodel import select

from src.repository import BaseRepository
from src.postgres import AsyncSession

from src.orders.models import Order
from src.orders.constants import OrderStatus


class OrdersRepository(BaseRepository[Order]):
    def __init__(self, postgres: AsyncSession):
        super().__init__(postgres, Order)

    async def get_by_status(self, status: OrderStatus, limit: int, offset: int):
        statement = select(Order).where(Order.status == status).offset(offset).limit(limit)
        db_orders = await self.postgres.exec(statement)
        db_orders = db_orders.all()
        return db_orders

    async def get_by_user_id(self, user_id: int, limit: int, offset: int):
        statement = select(Order).where(Order.user_id == user_id).offset(offset).limit(limit)
        db_orders = await self.postgres.exec(statement)
        db_orders = db_orders.all()
        return db_orders

    async def get_by_id_by_user_id(self, user_id: int, order_id: int):
        statement = select(Order).where(Order.user_id == user_id).where(Order.id == order_id)
        db_order = await self.postgres.exec(statement)
        db_order = db_order.first()
        return db_order

    async def update_by_id_by_user_id(self, user_id: int, order_id: int, order: Order, refresh: bool = True):
        db_order = await self.get_by_id_by_user_id(user_id, order_id)
        if not db_order:
            return None
        order_data = order.model_dump(exclude_unset=True)
        db_order.sqlmodel_update(order_data)
        self.postgres.add(db_order)
        await self.postgres.commit()
        if refresh:
            await self.postgres.refresh(db_order)
        return db_order

    async def delete_by_id_by_user_id(self, user_id: int, order_id: int):
        db_order = self.get_by_id_by_user_id(user_id, order_id)
        if not db_order:
            return None
        await self.postgres.delete(db_order)
        await self.postgres.commit()
        return db_order
