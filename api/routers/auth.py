from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from typing import Annotated

from models import User, UserCreate, Success, Token
from databases import Database
from dependencies import VerifyUser, verify_turnstile_token
from utils import pwd_context, generate_jwt
from tasks import send_email
from queues import low_queue


router = APIRouter(tags=["Authentication"], prefix="/auth")

@router.post("/register", status_code=201, response_model=Success, dependencies=[Depends(verify_turnstile_token)])
def register(db: Database, user: UserCreate):
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already in use")
    low_queue.enqueue(send_email, "", user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"username": user.username, "token": generate_jwt({"sub": db_user.id}, audience="verify")})
    return {"message": "Verification email sent"}

@router.post("/login", response_model=Token, dependencies=[Depends(verify_turnstile_token)])
def login(db: Database, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    statement = select(User).where(or_(User.username == form_data.username, User.email == form_data.username))
    db_user = db.exec(statement).first()
    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not db_user.is_verified:
        raise HTTPException(status_code=400, detail="User not verified")
    return {"access_token": generate_jwt({"sub": db_user.id}, secret=db_user.password)}

@router.post("/logout", response_model=Success)
def logout():
    return {"message": "User logged out"}

@router.post("/verify/{verify_token}", response_model=Success)
def verify(db: Database, verify_user: VerifyUser):
    if verify_user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    verify_user.is_verified = True
    db.add(verify_user)
    db.commit()
    return {"message": "User verified"}

@router.post("/forgot-password", response_model=Success, dependencies=[Depends(verify_turnstile_token)])
def forgot_password(db: Database, email: EmailStr):
    statement = select(User).where(User.email == email)
    db_user = db.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="User not active")
    low_queue.enqueue(send_email, "", db_user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"username": db_user.username, "token": generate_jwt({"sub": db_user.id}, audience="reset_password")})
    return {"message": "Password reset email sent"}

@router.post("/reset-password/{verify_token}", response_model=Success)
def reset_password(db: Database, verify_user: VerifyUser, password: str):
    verify_user.password = pwd_context.hash(password)
    db.add(verify_user)
    db.commit()
    return {"message": "Password reset"}