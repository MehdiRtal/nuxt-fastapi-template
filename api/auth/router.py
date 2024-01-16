from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from typing import Annotated

from models import DefaultResponse
from users.models import User, UserCreate
from database import Database
from utils import send_email
from dependencies import valid_turnstile_token

from .utils import generate_access_token, generate_verify_token, pwd_context, oauth
from .models import AccessToken
from .dependencies import VerifyUser,  blacklist_access_token


router = APIRouter(tags=["Authentication"], prefix="/auth")

@router.post("/register", status_code=201, dependencies=[Depends(valid_turnstile_token)])
async def register(db: Database, user: UserCreate) -> DefaultResponse:
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        raise HTTPException(400, "User already exists")
    verify_token = generate_verify_token(db_user.id, audience="verify")
    send_email("", user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"full_name": user.full_name, "token": verify_token})
    return {"message": "Verification email sent"}

@router.post("/verify/{verify_token}")
async def verify(db: Database, verify_user: VerifyUser) -> DefaultResponse:
    if verify_user.is_verified:
        raise HTTPException(400, "User already verified")
    verify_user.is_verified = True
    db.add(verify_user)
    await db.commit()
    return {"message": "User verified"}

@router.post("/login", dependencies=[Depends(valid_turnstile_token)])
async def login(db: Database, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> AccessToken:
    statement = select(User).where(User.email == form_data.username)
    db_user = await db.exec(statement)
    db_user = db_user.first()
    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(400, "Incorrect username or password")
    if not db_user.is_verified:
        raise HTTPException(400, "User not verified")
    access_token = generate_access_token(db_user.id, secret=db_user.password)
    return {"access_token": access_token}

@router.post("/sso/google")
async def sso_google(request: Request) -> dict:
    callback_url = request.url_for("sso_google_callback")
    return await oauth.google.authorize_redirect(request, callback_url)

@router.get("/sso/google/callback")
async def sso_google_callback(request: Request, db: Database) -> AccessToken | dict:
    try:
        user_info = await oauth.google.authorize_access_token(request)
        user = UserCreate()
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        verify_token = generate_verify_token(db_user.id, audience="reset_password")
        return {"verify_token": verify_token}
    except IntegrityError:
        access_token = generate_access_token(db_user.id, secret=db_user.password)
        return {"access_token": access_token}

@router.post("/logout", dependencies=[Depends(blacklist_access_token)])
async def logout() -> DefaultResponse:
    return {"message": "User logged out"}

@router.post("/forgot-password", dependencies=[Depends(valid_turnstile_token)])
async def forgot_password(db: Database, email: EmailStr) -> DefaultResponse:
    statement = select(User).where(User.email == email)
    db_user = await db.exec(statement)
    db_user = db_user.first()
    if not db_user:
        raise HTTPException(404, "User not found")
    if not db_user.is_active:
        raise HTTPException(400, "User not active")
    verify_token = generate_verify_token(db_user.id, audience="reset_password")
    send_email("", db_user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"full_name": db_user.full_name, "token": verify_token})
    return {"message": "Password reset email sent"}

@router.post("/reset-password/{verify_token}")
async def reset_password(db: Database, verify_user: VerifyUser, password: str) -> DefaultResponse:
    verify_user.password = pwd_context.hash(password)
    db.add(verify_user)
    await db.commit()
    return {"message": "Password reset"}
