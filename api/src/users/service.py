from fastapi import Request

from src.auth.utils import verify_password, hash_password, google_oauth_client
from src.items.models import Item
from src.auth.exceptions import InvalidCredentials
from src.items.repository import ItemsRepository
from src.exceptions import EntityNotFound, EntityAlreadyExists

from src.users.models import User
from src.users.exceptions import UserNotFound, UserAlreadyExists, UserOAuthNotLinked
from src.users.utils import create_payment
from src.users.repository import UsersRepository


class UsersService:
    def __init__(self, users_repository: UsersRepository, items_repository: ItemsRepository):
        self.users_repository = users_repository
        self.items_repository = items_repository

    async def change_current_user_password(self, current_user: User, current_password: str, new_password: str):
        if not verify_password(current_password, current_user.password):
            raise InvalidCredentials()
        current_user.password = hash_password(new_password)
        current_user = await self.users_repository.update(current_user)
        return current_user

    async def unlink_current_user_google(self, current_user: User):
        if not current_user.google_oauth_refresh_token:
            raise UserOAuthNotLinked()
        await google_oauth_client.revoke_token(current_user.google_oauth_refresh_token, "refresh_token")
        current_user.google_oauth_refresh_token = None
        current_user = await self.users_repository.update(current_user)
        return current_user

    async def add_current_user_payment(self, request: Request, current_user: User, value: float) -> dict:
        callback_url = request.url_for("current_user_payment_callback")
        payment = create_payment(value, current_user.email, {"user_id": current_user.id}, callback_url)
        return {"payment_url": payment["data"]["url"]}

    async def current_user_payment_callback(self, request: Request):
        body = await request.json()
        user_id = body["data"]["custom_fields"]["user_id"]
        db_user = await self.users_repository.get_by_id(user_id)
        db_user.balance += body["data"]["value"]
        await self.users_repository.update(db_user)
        return {"message": "Payment received"}

    async def get_current_user_items(self, current_user: User, limit: int = 100, offset: int = 0):
        db_items = await self.items_repository.get_by_user_id(current_user.id, limit, offset)
        return db_items

    async def get_current_user_item(self, current_user: User, item_id: int):
        db_item = await self.items_repository.get_by_id_by_user_id(current_user.id, item_id)
        return db_item

    async def add_current_user_item(self, current_user: User, item: Item):
        item.user_id = current_user.id
        db_item = await self.items_repository.add(item)
        return db_item

    async def update_current_user_item(self, current_user: User, item_id: int, item: Item):
        db_item = await self.items_repository.update_by_id_by_user_id(current_user.id, item_id, item)
        return db_item

    async def delete_current_user_item(self, current_user: User, item_id: int):
        db_item = await self.items_repository.delete_by_id_by_user_id(current_user.id, item_id)
        return db_item

    async def get_current_user(self, current_user: User):
        return current_user

    async def update_current_user(self, current_user: User, user: User):
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(current_user, key, value)
        current_user = await self.users_repository.update(current_user)
        return current_user

    async def delete_current_user(self, current_user: User):
        current_user.is_active = False
        current_user = await self.users_repository.update(current_user)
        return current_user

    async def get_users(self, limit: int, offset: int):
        try:
            db_users = await self.users_repository.get(limit, offset)
        except EntityNotFound:
            raise UserNotFound
        return db_users

    async def get_user(self, user_id: int):
        try:
            db_user = await self.users_repository.get_by_id(user_id)
        except EntityNotFound:
            raise UserNotFound
        return db_user

    async def add_user(self, user: User):
        try:
            db_user = await self.users_repository.add(user)
        except EntityAlreadyExists:
            raise UserAlreadyExists
        return db_user

    async def update_user(self, user_id: int, user: User):
        try:
            db_user = await self.users_repository.update_by_id(user_id, user)
        except EntityNotFound:
            raise UserNotFound
        return db_user

    async def delete_user(self, user_id: int):
        try:
            db_user = await self.users_repository.delete_by_id(user_id)
        except EntityNotFound:
            raise UserNotFound
        return db_user
