from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.exc import IntegrityError

from models import User, UserCreate, UserRead, UserUpdate
from databases import Database
from dependencies import CurrentUser
from utils import pwd_context


router = APIRouter(tags=["Users"], prefix="/users")

@router.post("/me/change-password", response_model=UserRead)
def change_current_user_password(db: Database, current_user: CurrentUser, current_password: str, new_password: str):
    if not pwd_context.verify(current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    current_user.password = pwd_context.hash(new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me", response_model=UserRead)
def get_current_user(current_user: CurrentUser):
    return current_user

@router.patch("/me", response_model=UserRead)
def update_current_user(db: Database, current_user: CurrentUser, user: UserUpdate):
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me", response_model=UserRead)
def delete_current_user(db: Database, current_user: CurrentUser):
    current_user.is_active = False
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/", response_model=List[UserRead])
def get_users(db: Database, limit: int = 100, offset: int = 0):
    db_users = db.query(User).offset(offset).limit(limit).all()
    if not db_users:
        raise HTTPException(status_code=404, detail="No users found")
    return db_users

@router.get("/{user_id}", response_model=UserRead)
def get_user(db: Database, user_id: int):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/", status_code=201, response_model=UserRead)
def add_user(db: Database, user: UserCreate):
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(db: Database, user_id: int, user: UserUpdate):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(db: Database, user_id: int):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user