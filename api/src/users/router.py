from fastapi import APIRouter, Depends, Request

from src.auth.dependencies import CurrentUser
from src.items.models import ItemCreate, ItemRead, ItemUpdate
from src.auth.dependencies import require_superuser
from src.models import DefaultResponse

from src.users.models import UserCreate, UserRead, UserUpdate
from src.users.dependencies import valid_sellix_signature, UsersServiceSession
from src.users.service import UsersService


router = APIRouter(tags=["Users"], prefix="/users")

@router.post("/me/change-password")
async def change_current_user_password(users_service: UsersServiceSession, current_user: CurrentUser, current_password: str, new_password: str) -> UserRead:
    return await users_service.change_current_user_password(current_user, current_password, new_password)

@router.post("/me/unlink/google")
async def unlink_current_user_google(users_service: UsersServiceSession, current_user: CurrentUser) -> UserRead:
    return await users_service.unlink_current_user_google(current_user)

@router.post("/me/payment")
async def add_current_user_payment(request: Request, users_service: UsersServiceSession, current_user: CurrentUser, value: float) -> dict:
    return await users_service.add_current_user_payment(request, current_user, value)

@router.get("/me/payment/callback", dependencies=[Depends(valid_sellix_signature)])
async def current_user_payment_callback(request: Request, users_service: UsersServiceSession) -> DefaultResponse:
    return await users_service.current_user_payment_callback(request)

@router.get("/me/items")
async def get_current_user_items(users_service: UsersServiceSession, current_user: CurrentUser, limit: int = 100, offset: int = 0) -> list[ItemRead]:
    return await users_service.get_current_user_items(current_user, limit, offset)

@router.get("/me/items/{item_id}")
async def get_current_user_item(users_service: UsersServiceSession, current_user: CurrentUser, item_id: int) -> ItemRead:
    return await users_service.get_current_user_item(current_user, item_id)

@router.post("/me/items", status_code=201)
async def add_current_user_item(users_service: UsersServiceSession, current_user: CurrentUser, item: ItemCreate) -> ItemRead:
    return await users_service.add_current_user_item(current_user, item)

@router.patch("/me/items/{item_id}")
async def update_current_user_item(users_service: UsersServiceSession, current_user: CurrentUser, item_id: int, item: ItemUpdate) -> ItemRead:
    return await users_service.update_current_user_item(current_user, item_id, item)

@router.delete("/me/items/{item_id}")
async def delete_current_user_item(users_service: UsersServiceSession, current_user: CurrentUser, item_id: int) -> ItemRead:
    return await users_service.delete_current_user_item(current_user, item_id)

@router.get("/me")
async def get_current_user(current_user: CurrentUser) -> UserRead:
    users_service = UsersService()
    return await users_service.get_current_user(current_user)

@router.patch("/me")
async def update_current_user(users_service: UsersServiceSession, current_user: CurrentUser, user: UserUpdate) -> UserRead:
    return await users_service.update_current_user(current_user, user)

@router.delete("/me")
async def delete_current_user(users_service: UsersServiceSession, current_user: CurrentUser) -> UserRead:
    return await users_service.delete_current_user(current_user)

@router.get("/")
async def get_users(users_service: UsersServiceSession, limit: int = 100, offset: int = 0) -> list[UserRead]:
    return await users_service.get_users(limit, offset)

@router.get("/{user_id}")
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
