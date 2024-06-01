from src.orders.models import Order
from src.orders.exceptions import OrderNotFound
from src.orders.repository import OrdersRepository


class OrdersService:
    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository

    async def get_orders(self, limit: int, offset: int):
        db_orders = await self.orders_repository.get(limit, offset)
        if not db_orders:
            raise OrderNotFound
        return db_orders

    async def get_order(self, order_id: int):
        db_order = await self.orders_repository.get_by_id(order_id)
        if not db_order:
            raise OrderNotFound
        return db_order

    async def add_order(self, order: Order):
        db_order = await self.orders_repository.add(order)
        return db_order

    async def update_order(self, order_id: int, order: Order):
        db_order = await self.orders_repository.update_by_id(order_id, order)
        if not db_order:
            raise OrderNotFound
        return db_order

    async def delete_order(self, order_id: int):
        db_order = await self.orders_repository.delete_by_id(order_id)
        if not db_order:
            raise OrderNotFound
        return db_order
