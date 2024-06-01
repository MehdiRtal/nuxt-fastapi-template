from fastapi import APIRouter, Depends

from src.auth.dependencies import CurrentUser
from src.auth.dependencies import require_superuser

from src.users.models import UserCreate, UserRead, UserUpdate, UserReadPublic, UserUpdatePublic
from src.users.dependencies import UsersServiceSession
from src.orders.models import OrderRead, OrderCreate, OrderUpdate, OrderCreatePublic

router = APIRouter(tags=["Users"], prefix="/users")


@router.put("/me/change-password")
async def change_current_user_password(users_service: UsersServiceSession, current_user: CurrentUser, current_password: str, password: str) -> UserReadPublic:
    return await users_service.change_current_user_password(current_user, current_password, password)

@router.get("/me")
async def get_current_user(users_service: UsersServiceSession, current_user: CurrentUser) -> UserReadPublic:
    return await users_service.get_current_user(current_user)

@router.patch("/me")
async def update_current_user(users_service: UsersServiceSession, current_user: CurrentUser, user: UserUpdatePublic) -> UserReadPublic:
    return await users_service.update_current_user(current_user, user)

@router.delete("/me")
async def deactivate_current_user(users_service: UsersServiceSession, current_user: CurrentUser) -> UserReadPublic:
    return await users_service.deactivate_current_user(current_user)

@router.post("/me/orders", status_code=201)
async def add_current_user_order(users_service: UsersServiceSession, current_user: CurrentUser, order: OrderCreatePublic) -> OrderRead:
    return await users_service.add_current_user_order(current_user, order)

@router.delete("/me/orders/{order_id}")
async def cancel_current_user_order(users_service: UsersServiceSession, current_user: CurrentUser, order_id: int) -> OrderRead:
    return await users_service.cancel_current_user_order(current_user, order_id)

@router.get("/{user_id}/orders", dependencies=[Depends(require_superuser)])
async def get_user_orders(users_service: UsersServiceSession, user_id: int, limit: int = 100, offset: int = 0) -> list[OrderRead]:
    return await users_service.get_user_orders(user_id, limit, offset)

@router.get("/{user_id}/orders/{order_id}", dependencies=[Depends(require_superuser)])
async def get_user_order(users_service: UsersServiceSession, user_id: int, order_id: int) -> OrderRead:
    return await users_service.get_user_order(user_id, order_id)

@router.post("/{user_id}/orders", status_code=201, dependencies=[Depends(require_superuser)])
async def add_user_order(users_service: UsersServiceSession, user_id: int, order: OrderCreate) -> OrderRead:
    return await users_service.add_user_order(user_id, order)

@router.patch("/{user_id}/orders/{order_id}", dependencies=[Depends(require_superuser)])
async def update_user_order(users_service: UsersServiceSession, user_id: int, order_id: int, order: OrderUpdate) -> OrderRead:
    return await users_service.update_user_order(user_id, order_id, order)

@router.delete("/{user_id}/orders/{order_id}", dependencies=[Depends(require_superuser)])
async def delete_user_order(users_service: UsersServiceSession, user_id: int, order_id: int) -> OrderRead:
    return await users_service.delete_user_order(user_id, order_id)

@router.get("/", dependencies=[Depends(require_superuser)])
async def get_users(users_service: UsersServiceSession, limit: int = 100, offset: int = 0) -> list[UserRead]:
    return await users_service.get_users(limit, offset)

@router.get("/{user_id}", dependencies=[Depends(require_superuser)])
async def get_user(users_service: UsersServiceSession, user_id: int):
    return await users_service.get_user(user_id)

@router.post("/", status_code=201, dependencies=[Depends(require_superuser)])
async def add_user(users_service: UsersServiceSession, user: UserCreate) -> UserRead:
    return await users_service.add_user(user)

@router.patch("/{user_id}", dependencies=[Depends(require_superuser)])
async def update_user(users_service: UsersServiceSession, user_id: int, user: UserUpdate) -> UserRead:
    return await users_service.update_user(user_id, user)

@router.delete("/{user_id}", dependencies=[Depends(require_superuser)])
async def delete_user(users_service: UsersServiceSession, user_id: int) -> UserRead:
    return await users_service.delete_user(user_id)
