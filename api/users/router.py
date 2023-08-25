from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_restful.cbv import cbv
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from database import Database
from auth.utils import pwd_context
from auth.dependencies import CurrentUser

from .models import User, UserCreate, UserRead, UserUpdate


router = APIRouter(tags=["Users"], prefix="/users")

@cbv(router)
class Users:
    db: Database

    @router.get("/me")
    def get_current_user(current_user: CurrentUser):
        return current_user

    @router.patch("/me")
    async def update_current_user(self, current_user: CurrentUser, user: UserUpdate) -> UserRead:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(current_user, key, value)
        self.db.add(current_user)
        await self.db.commit()
        await self.db.refresh(current_user)
        return current_user

    @router.delete("/me")
    async def delete_current_user(self, current_user: CurrentUser) -> UserRead:
        current_user.is_active = False
        self.db.add(current_user)
        await self.db.commit()
        await self.db.refresh(current_user)
        return current_user

    @router.post("/me/change-password")
    async def change_current_user_password(self, current_user: CurrentUser, current_password: str, new_password: str) -> UserRead:
        if not pwd_context.verify(current_password, current_user.password):
            raise HTTPException(400, "Incorrect password")
        current_user.password = pwd_context.hash(new_password)
        self.db.add(current_user)
        await self.db.commit()
        await self.db.refresh(current_user)
        return current_user

    @router.get("/")
    async def get_users(self, limit: int = 100, offset: int = 0) -> list[UserRead]:
        statement = select(User).offset(offset).limit(limit)
        db_users = await self.db.exec(statement)
        db_users = db_users.all()
        if not db_users:
            raise HTTPException(404, "No users found")
        return db_users

    @router.get("/{user_id}")
    async def get_user(self, user_id: int):
        db_user = await self.db.get(User, user_id)
        if not db_user:
            raise HTTPException(404, "User not found")
        return db_user

    @router.post("/", status_code=201)
    async def add_user(self, user: UserCreate) -> UserRead:
        try:
            user.password = pwd_context.hash(user.password)
            db_user = User(**user.model_dump())
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
        except IntegrityError:
            raise HTTPException(400, "User already exists")
        return db_user

    @router.patch("/{user_id}")
    async def update_user(self, user_id: int, user: UserUpdate) -> UserRead:
        db_user = await self.db.get(User, user_id)
        if not db_user:
            raise HTTPException(404, "User not found")
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    @router.delete("/{user_id}")
    async def delete_user(self, user_id: int) -> UserRead:
        db_user = await self.db.get(User, user_id)
        if not db_user:
            raise HTTPException(404, "User not found")
        self.db.delete(db_user)
        await self.db.commit()
        return db_user