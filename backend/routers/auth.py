from fastapi import APIRouter, HTTPException, Response, Depends, Form
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr

from models import User, UserCreate, UserRead
from database import Database
from dependencies import VerifyUser, verify_turnstile_token
from utils import pwd_context, generate_jwt, send_verify


router = APIRouter(tags=["Authentication"], prefix="/auth")

@router.post("/register", status_code=201, response_model=UserRead, dependencies=[Depends(verify_turnstile_token)])
def register(db: Database, user: UserCreate):
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already in use")
    return {"verification_sid": send_verify(email_to=db_user.email)}

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
    return {"status": "success", "message": "Logged out"}

@router.post("/verify/{verification_sid}")
def verify(db: Database, verify_user: VerifyUser):
    if verify_user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    verify_user.is_verified = True
    db.add(verify_user)
    db.commit()
    return {"status": "success", "message": "User verified"}

@router.post("/forgot-password", dependencies=[Depends(verify_turnstile_token)])
def forgot_password(db: Database, email: EmailStr):
    statement = select(User).where(User.email == email)
    db_user = db.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_user.is_active:
        raise HTTPException(status_code=400, detail="User not active")
    return {"verification_sid": send_verify(email_to=db_user.email)}

@router.post("/reset-password/{verification_sid}")
def reset_password(db: Database, verify_user: VerifyUser, password: str):
    verify_user.password = pwd_context.hash(password)
    db.add(verify_user)
    db.commit()
    return {"status": "success", "message": "Password reset"}