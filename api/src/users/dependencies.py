from fastapi import Request, Depends
from fastapi.param_functions import Header
from fastapi.exceptions import HTTPException
import hmac
import hashlib
from typing import Annotated

from src.config import settings
from src.postgres import PostgresSession
from src.items.repository import ItemsRepository

from src.users.repository import UsersRepository
from src.users.service import UsersService


def get_users_service_session(postgres: PostgresSession):
    users_repository = UsersRepository(postgres)
    items_repository = ItemsRepository(postgres)
    users_service = UsersService(users_repository, items_repository)
    return users_service

UsersServiceSession = Annotated[UsersService, Depends(get_users_service_session)]

async def valid_sellix_signature(request: Request, x_sellix_signature: Annotated[str, Header()] = None):
    if settings.ENVIRONEMENT.is_dev:
        return
    body = await request.body()
    signature = hmac.new(bytes(settings.SELLIX_SIGNATURE_SECRET), body, hashlib.sha512).hexdigest()
    if not hmac.compare_digest(signature, x_sellix_signature):
        raise HTTPException(403, "Invalid signature")
