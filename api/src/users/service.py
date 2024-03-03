from fastapi import Request
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from src.db import DBSession
from src.auth.utils import verify_password, hash_password, google_oauth_client
from src.auth.dependencies import CurrentUser
from src.items.models import Item, ItemCreate, ItemRead, ItemUpdate
from src.items.exceptions import ItemNotFound
from src.auth.exceptions import InvalidCredentials
from src.models import DefaultResponse

from src.users.models import User, UserCreate, UserRead, UserUpdate
from src.users.exceptions import UserNotFound, UserAlreadyExists, UserOAuthNotLinked
from src.users.utils import create_payment


class UsersService:
    def __init__(self, db: DBSession | None = None):
        self.db = db

    async def change_current_user_password(self, current_user: CurrentUser, current_password: str, new_password: str) -> UserRead:
        if not verify_password(current_password, current_user.password):
            raise InvalidCredentials()
        current_user.password = hash_password(new_password)
        self.db.add(current_user)
        await self.db.commit()
        await self.db.refresh(current_user)
        return current_user

    async def unlink_current_user_google(self, current_user: CurrentUser) -> UserRead:
        if not current_user.google_oauth_refresh_token:
            raise UserOAuthNotLinked()
        await google_oauth_client.revoke_token(current_user.google_oauth_refresh_token, "refresh_token")
        current_user.google_oauth_refresh_token = None
        self.db.add(current_user)
        await self.db.commit()
        await self.db.refresh(current_user)
        return current_user

    async def add_current_user_payment(self, request: Request, current_user: CurrentUser, value: float) -> dict:
        callback_url = request.url_for("current_user_payment_callback")
        payment = create_payment(value, current_user.email, {"user_id": current_user.id}, callback_url)
        return {"payment_url": payment["data"]["url"]}

    async def current_user_payment_callback(self, request: Request) -> DefaultResponse:
        body = await request.json()
        db_user = await self.db.get(User, body["data"]["custom_fields"]["user_id"])
        db_user.balance += body["data"]["value"]
        self.db.add(db_user)
        await self.db.commit()
        return {"message": "Payment received"}

    async def get_current_user_items(self, current_user: CurrentUser, limit: int = 100, offset: int = 0) -> list[ItemRead]:
        statement = select(Item).where(Item.user_id == current_user.id).offset(offset).limit(limit)
        db_items = await self.db.exec(statement)
        db_items = db_items.all()
        if not db_items:
            raise ItemNotFound()
        return db_items

    async def get_current_user_item(self, current_user: CurrentUser, item_id: int) -> ItemRead:
        statement = select(Item).where(Item.user_id == current_user.id).where(Item.id == item_id)
        db_item = await self.db.exec(statement)
        db_item = db_item.first()
        if not db_item:
            raise ItemNotFound()
        return db_item

    async def add_current_user_item(self, current_user: CurrentUser, item: ItemCreate) -> ItemRead:
        item.user_id = current_user.id
        db_item = Item(**item.model_dump())
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def update_current_user_item(self, current_user: CurrentUser, item_id: int, item: ItemUpdate) -> ItemRead:
        statement = select(Item).where(Item.user_id == current_user.id).where(Item.id == item_id)
        db_item = await self.db.exec(statement)
        db_item = db_item.first()
        if not db_item:
            raise ItemNotFound()
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        await self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def delete_current_user_item(self, current_user: CurrentUser, item_id: int) -> ItemRead:
        statement = select(Item).where(Item.user_id == current_user.id).where(Item.id == item_id)
        db_item = await self.db.exec(statement)
        db_item = db_item.first()
        if not db_item:
            raise ItemNotFound()
        await self.db.delete(db_item)
        await self.db.commit()
        return db_item

    async def get_current_user(self, current_user: CurrentUser) -> UserRead:
        return current_user

    async def update_current_user(self, current_user: CurrentUser, user: UserUpdate) -> UserRead:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(current_user, key, value)
        self.db.add(current_user)
        await self.db.commit()
        await self.db.refresh(current_user)
        return current_user

    async def delete_current_user(self, current_user: CurrentUser) -> UserRead:
        current_user.is_active = False
        self.db.add(current_user)
        await self.db.commit()
        await self.db.refresh(current_user)
        return current_user

    async def get_users(self, limit: int, offset: int) -> list[UserRead]:
        statement = select(User).offset(offset).limit(limit)
        db_users = await self.db.exec(statement)
        db_users = db_users.all()
        if not db_users:
            raise UserNotFound()
        return db_users

    async def get_user(self, user_id: int) -> UserRead:
        db_user = await self.db.get(User, user_id)
        if not db_user:
            raise UserNotFound()
        return db_user

    async def add_user(self, user: UserCreate) -> UserRead:
        try:
            user.password = hash_password(user.password)
            db_user = User(**user.model_dump())
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
        except IntegrityError:
            raise UserAlreadyExists()
        return db_user

    async def update_user(self, user_id: int, user: UserUpdate) -> UserRead:
        db_user = await self.db.get(User, user_id)
        if not db_user:
            raise UserNotFound()
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int) -> UserRead:
        db_user = await self.db.get(User, user_id)
        if not db_user:
            raise UserNotFound()
        self.db.delete(db_user)
        await self.db.commit()
        return db_user
