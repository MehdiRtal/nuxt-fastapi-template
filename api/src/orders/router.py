from fastapi import APIRouter, Depends

from src.auth.dependencies import require_superuser

from src.orders.models import OrderCreate, OrderRead, OrderUpdate
from src.orders.dependencies import OrdersServiceSession


router = APIRouter(tags=["Orders"], prefix="/orders")


@router.get("/", dependencies=[Depends(require_superuser)])
async def get_orders(orders_service: OrdersServiceSession, limit: int = 100, offset: int = 0) -> list[OrderRead]:
    return await orders_service.get_orders(limit, offset)

@router.get("/{order_id}", dependencies=[Depends(require_superuser)])
async def get_order(orders_service: OrdersServiceSession, order_id: int):
    return await orders_service.get_order(order_id)

@router.post("/", status_code=201, dependencies=[Depends(require_superuser)])
async def add_order(orders_service: OrdersServiceSession, order: OrderCreate) -> OrderRead:
    return await orders_service.add_order(order)

@router.patch("/{order_id}", dependencies=[Depends(require_superuser)])
async def update_order(orders_service: OrdersServiceSession, order_id: int, order: OrderUpdate) -> OrderRead:
    return await orders_service.update_order(order_id, order)

@router.delete("/{order_id}", dependencies=[Depends(require_superuser)])
async def delete_order(orders_service: OrdersServiceSession, order_id: int) -> OrderRead:
    return await orders_service.delete_order(order_id)
