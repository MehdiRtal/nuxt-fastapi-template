from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from typing import Annotated

from models import DefaultResponse
from users.models import User, UserCreate
from users.exceptions import UserAlreadyExists, UserNotVerified, UserNotActive, UserNotFound, UserAlreadyVerified, UserOAuthNotLinked
from db import DBSession
from utils import send_email
from dependencies import valid_turnstile_token

from .utils import generate_access_token, generate_verify_token, pwd_context, google_oauth_client
from .models import AccessToken
from .dependencies import VerifyUser, blacklist_access_token, GoogleOAuthCallback
from .exceptions import InvalidCredentials


router = APIRouter(tags=["Authentication"], prefix="/auth")

@router.post("/register", status_code=201, dependencies=[Depends(valid_turnstile_token)])
async def register(db: DBSession, user: UserCreate) -> DefaultResponse:
    try:
        user.password = pwd_context.hash(user.password)
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        raise UserAlreadyExists()
    verify_token = generate_verify_token(db_user.id, audience="verify")
    send_email("", user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"full_name": user.full_name, "token": verify_token})
    return {"message": "Verification email sent"}

@router.post("/verify/{verify_token}")
async def verify(db: DBSession, verify_user: VerifyUser) -> DefaultResponse:
    if verify_user.is_verified:
        raise UserAlreadyVerified()
    verify_user.is_verified = True
    db.add(verify_user)
    await db.commit()
    return {"message": "User verified"}

@router.post("/login", dependencies=[Depends(valid_turnstile_token)])
async def login(db: DBSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> AccessToken:
    statement = select(User).where(User.email == form_data.username)
    db_user = await db.exec(statement)
    db_user = db_user.first()
    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise InvalidCredentials()
    if not db_user.is_verified:
        raise UserNotVerified()
    access_token = generate_access_token(db_user.id, secret=db_user.password)
    return {"access_token": access_token}

@router.get("/sso/google")
async def sso_google(request: Request) -> dict:
    callback_url = request.url_for("sso_google_callback")
    authorization_url = await google_oauth_client.get_authorization_url(callback_url)
    return {"authorization_url": authorization_url}

@router.get("/sso/google/callback")
async def sso_google_callback(db: DBSession, callback: GoogleOAuthCallback) -> AccessToken | dict:
    token, state = callback
    id, email = await google_oauth_client.get_id_email(token["access_token"])
    statement = select(User).where(User.email == email)
    db_user = await db.exec(statement)
    db_user = db_user.first()
    if db_user:
        if not db_user.google_oauth_refresh_token:
            raise UserOAuthNotLinked()
        db_user.google_oauth_refresh_token = token["refresh_token"]
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        access_token = generate_access_token(db_user.id, secret=db_user.password)
        return {"access_token": access_token}
    else:
        db_user = User(full_name="", email=email, password="", google_oauth_refresh_token=token["refresh_token"])
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        verify_token = generate_verify_token(db_user.id, audience="reset_password")
        return {"verify_token": verify_token}

@router.get("/link/google")
async def link_google(request: Request) -> dict:
    callback_url = request.url_for("link_google_callback")
    authorization_url = await google_oauth_client.get_authorization_url(callback_url)
    return {"authorization_url": authorization_url}

@router.get("/link/google/callback")
async def link_google_callback(db: DBSession, callback: GoogleOAuthCallback) -> DefaultResponse:
    token, state = callback
    id, email = await google_oauth_client.get_id_email(token["access_token"])
    statement = select(User).where(User.email == email)
    db_user = await db.exec(statement)
    db_user = db_user.first()
    if not db_user:
        raise UserNotFound()
    if not db_user.is_verified:
        raise UserNotVerified()
    if not db_user.is_active:
        raise UserNotActive()
    db_user.google_oauth_refresh_token = token["refresh_token"]
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": "Google OAuth linked"}

@router.post("/logout", dependencies=[Depends(blacklist_access_token)])
async def logout() -> DefaultResponse:
    return {"message": "User logged out"}

@router.post("/forgot-password", dependencies=[Depends(valid_turnstile_token)])
async def forgot_password(db: DBSession, email: EmailStr) -> DefaultResponse:
    statement = select(User).where(User.email == email)
    db_user = await db.exec(statement)
    db_user = db_user.first()
    if not db_user:
        raise UserNotFound()
    if not db_user.is_active:
        raise UserNotActive()
    verify_token = generate_verify_token(db_user.id, audience="reset_password")
    send_email("", db_user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"full_name": db_user.full_name, "token": verify_token})
    return {"message": "Password reset email sent"}

@router.post("/reset-password/{verify_token}")
async def reset_password(db: DBSession, verify_user: VerifyUser, password: str) -> DefaultResponse:
    verify_user.password = pwd_context.hash(password)
    db.add(verify_user)
    await db.commit()
    return {"message": "Password reset"}
