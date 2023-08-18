from fastapi import APIRouter, HTTPException, Response, Depends, Form
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr

from models import User, UserCreate, UserRead, Success
from databases import Database
from dependencies import VerifyUser, verify_turnstile_token
from utils import pwd_context, generate_jwt, send_email
from queues import low_queue


router = APIRouter(tags=["Authentication"], prefix="/auth")

@router.post("/register", status_code=201, response_model=UserRead, dependencies=[Depends(verify_turnstile_token)])
def register(db: Database, user: UserCreate):
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already in use")
    low_queue.enqueue(send_email, "", user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"username": user.username, "token": generate_jwt({"user_id": db_user.id}, audience="verify")})
    return db_user

@router.post("/login", response_model=UserRead, dependencies=[Depends(verify_turnstile_token)])
def login(db: Database, response: Response, username: str = Form(), password: str = Form()):
    statement = select(User).where(or_(User.username == username, User.email == username))
    db_user = db.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if not db_user.is_verified:
        raise HTTPException(status_code=400, detail="User not verified")
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="User not active")
    response.set_cookie(key="session_id", value=generate_jwt({"user_id": db_user.id}))
    return db_user

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="session_id")
    return Success(message="User logged out")

@router.post("/verify/{token}")
def verify(db: Database, verify_user: VerifyUser):
    if verify_user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    verify_user.is_verified = True
    db.add(verify_user)
    db.commit()
    return Success(message="User verified")

@router.post("/forgot-password", dependencies=[Depends(verify_turnstile_token)])
def forgot_password(db: Database, email: EmailStr):
    statement = select(User).where(User.email == email)
    db_user = db.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="User not active")
    low_queue.enqueue(send_email, "", db_user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"username": db_user.username, "token": generate_jwt({"user_id": db_user.id}, audience="reset_password")})
    return Success(message="Password reset email sent")

@router.post("/reset-password/{token}")
def reset_password(db: Database, verify_user: VerifyUser, password: str):
    verify_user.password = pwd_context.hash(password)
    db.add(verify_user)
    db.commit()
    return Success(message="Password reset")