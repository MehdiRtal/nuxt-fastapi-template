from src.auth.utils import verify_password, hash_password
from src.auth.exceptions import InvalidCredentials

from src.users.models import User
from src.users.exceptions import UserNotFound, UserAlreadyExists, UserOAuthNotLinked
from src.users.repository import UsersRepository
from src.orders.repository import OrdersRepository
from src.orders.constants import OrderStatus
from src.orders.exceptions import OrderAlreadyFinished, OrderNotFound
from src.orders.models import Order

from src.auth.utils import google_oauth_client, apple_oauth_client


class UsersService:
    def __init__(self, users_repository: UsersRepository, orders_repository: OrdersRepository):
        self.users_repository = users_repository
        self.orders_repository = orders_repository

    async def change_current_user_password(self, current_user: User, current_password: str, password: str):
        if not verify_password(current_password, current_user.password):
            raise InvalidCredentials
        current_user.password = hash_password(password)
        current_user = await self.users_repository.update(current_user)
        return current_user

    async def unlink_current_user_google(self, current_user: User):
        if not current_user.google_oauth_refresh_token:
            raise UserOAuthNotLinked
        await google_oauth_client.revoke_token(current_user.google_oauth_refresh_token, "refresh_token")
        current_user.google_oauth_refresh_token = None
        current_user = await self.users_repository.update(current_user)
        return current_user

    async def unlink_current_user_apple(self, current_user: User):
        if not current_user.apple_oauth_refresh_token:
            raise UserOAuthNotLinked
        await apple_oauth_client.revoke_token(current_user.apple_oauth_refresh_token, "refresh_token")
        current_user.apple_oauth_refresh_token = None
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

    async def add_current_user_order(self, current_user: User, order: Order):
        extra_data = {
            "user_id": current_user.id,
        }
        db_order = await self.orders_repository.add(order, extra_data=extra_data)
        return db_order

    async def cancel_current_user_order(self, current_user: User, order_id: int):
        db_order = await self.get_user_order(current_user.id, order_id)
        if db_order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELED, OrderStatus.FAILED]:
            raise OrderAlreadyFinished
        db_order.status = OrderStatus.CANCELED
        db_order = await self.orders_repository.update(db_order)
        return db_order

    async def get_user_orders(self, user_id: int, limit: int, offset: int):
        db_orders = await self.orders_repository.get_by_user_id(user_id, limit, offset)
        if not db_orders:
            raise OrderNotFound
        return db_orders

    async def get_user_order(self, user_id: int, order_id: int):
        db_order = await self.orders_repository.get_by_id_by_user_id(user_id, order_id)
        if not db_order:
            raise OrderNotFound
        return db_order

    async def add_user_order(self, user_id: int, order: Order):
        order.user_id = user_id
        db_order = await self.orders_repository.add(order)
        return db_order

    async def update_user_order(self, user_id: int, order_id: int, order: Order):
        db_order = await self.orders_repository.update_by_id_by_user_id(user_id, order_id, order)
        if not db_order:
            raise OrderNotFound
        return db_order

    async def delete_user_order(self, user_id: int, order_id: int):
        db_order = await self.orders_repository.delete_by_id_by_user_id(user_id, order_id)
        if not db_order:
            raise OrderNotFound
        return db_order

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
