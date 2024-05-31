from src.auth.utils import verify_password, hash_password
from src.auth.exceptions import InvalidCredentials

from src.users.models import User
from src.users.exceptions import UserNotFound, UserAlreadyExists
from src.users.repository import UsersRepository


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def change_current_user_password(self, current_user: User, current_password: str, password: str):
        if not verify_password(current_password, current_user.password):
            raise InvalidCredentials
        current_user.password = hash_password(password)
        current_user = await self.users_repository.update(current_user)
        return current_user

    async def get_current_user(self, current_user: User):
        return current_user

    async def update_current_user(self, current_user: User, user: User):
        current_user.sqlmodel_update(user)
        db_user = await self.users_repository.update(current_user)
        return db_user

    async def deactivate_current_user(self, current_user: User):
        current_user.is_active = False
        current_user = await self.users_repository.update(current_user)
        return current_user

    async def get_users(self, limit: int, offset: int):
        db_users = await self.users_repository.get(limit, offset)
        if not db_users:
            raise UserNotFound
        return db_users

    async def get_user(self, user_id: int):
        db_user = await self.users_repository.get_by_id(user_id)
        if not db_user:
            raise UserNotFound
        return db_user

    async def add_user(self, user: User):
        user.password = hash_password(user.password)
        db_user = await self.users_repository.add(user)
        if not db_user:
            raise UserAlreadyExists
        return db_user

    async def update_user(self, user_id: int, user: User):
        db_user = await self.users_repository.update_by_id(user_id, user)
        if not db_user:
            raise UserNotFound
        return db_user

    async def delete_user(self, user_id: int):
        db_user = await self.users_repository.delete_by_id(user_id)
        if not db_user:
            raise UserNotFound
        return db_user
