from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError

from models import User, UserCreate, UserRead, UserUpdate
from databases import Database
from dependencies import CurrentUser
from utils import pwd_context


router = APIRouter(tags=["Users"], prefix="/users")

@cbv(router)
class Users:
    db: Database

    @router.post("/me/change-password")
    def change_current_user_password(self, current_user: CurrentUser, current_password: str, new_password: str) -> UserRead:
        if not pwd_context.verify(current_password, current_user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        current_user.password = pwd_context.hash(new_password)
        self.db.add(current_user)
        self.db.commit()
        self.db.refresh(current_user)
        return current_user

    @router.get("/me")
    def get_current_user(current_user: CurrentUser):
        return current_user

    @router.patch("/me")
    def update_current_user(self, current_user: CurrentUser, user: UserUpdate) -> UserRead:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(current_user, key, value)
        self.db.add(current_user)
        self.db.commit()
        self.db.refresh(current_user)
        return current_user

    @router.delete("/me")
    def delete_current_user(self, current_user: CurrentUser) -> UserRead:
        current_user.is_active = False
        self.db.add(current_user)
        self.db.commit()
        self.db.refresh(current_user)
        return current_user

    @router.get("/")
    def get_users(self, limit: int = 100, offset: int = 0) -> list[UserRead]:
        db_users = self.db.query(User).offset(offset).limit(limit).all()
        if not db_users:
            raise HTTPException(status_code=404, detail="No users found")
        return db_users

    @router.get("/{user_id}")
    def get_user(self, user_id: int):
        db_user = self.db.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    @router.post("/", status_code=201)
    def add_user(self, user: UserCreate) -> UserRead:
        try:
            user.password = pwd_context.hash(user.password)
            db_user = User(**user.model_dump())
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")
        return db_user

    @router.patch("/{user_id}")
    def update_user(self, user_id: int, user: UserUpdate) -> UserRead:
        db_user = self.db.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    @router.delete("/{user_id}")
    def delete_user(self, user_id: int) -> UserRead:
        db_user = self.db.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(db_user)
        self.db.commit()
        return db_user