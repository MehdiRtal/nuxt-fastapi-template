from fastapi import Depends
from typing import Annotated

from src.postgres import PostgresSession

from src.orders.repository import OrdersRepository
from src.orders.service import OrdersService


def get_orders_service_session(postgres: PostgresSession):
    orders_repository = OrdersRepository(postgres)
    return OrdersService(orders_repository)

OrdersServiceSession = Annotated[OrdersService, Depends(get_orders_service_session)]
