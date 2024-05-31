from fastapi import Depends
from typing import Annotated

from src.postgres import PostgresSession

from src.users.repository import UsersRepository
from src.users.service import UsersService


def get_users_service_session(postgres: PostgresSession):
    users_repository = UsersRepository(postgres)
    return UsersService(users_repository)

UsersServiceSession = Annotated[UsersService, Depends(get_users_service_session)]
