from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_restful.cbv import cbv
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from typing import Annotated

from models import DefaultResponse
from users.models import User, UserCreate
from database import Database
from utils import send_email
from dependencies import valid_turnstile_token

from .utils import generate_access_token, generate_verify_token, pwd_context
from .models import Token
from .dependencies import VerifyUser,  blacklist_access_token


router = APIRouter(tags=["Authentication"], prefix="/auth")

@cbv(router)
class AuthRouter:
    db: Database

    @router.post("/register", status_code=201, dependencies=[Depends(valid_turnstile_token)])
    async def register(self, user: UserCreate) -> DefaultResponse:
        try:
            user.password = pwd_context.hash(user.password)
            db_user = User(**user.model_dump())
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
        except IntegrityError:
            raise HTTPException(400, "Username or email already in use")
        send_email("", user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"username": user.username, "token": generate_verify_token(db_user.id, audience="verify")})
        return {"message": "Verification email sent"}

    @router.post("/login", dependencies=[Depends(valid_turnstile_token)])
    async def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
        statement = select(User).where(or_(User.username == form_data.username, User.email == form_data.username))
        db_user = await self.db.exec(statement)
        db_user = db_user.first()
        if not db_user or not pwd_context.verify(form_data.password, db_user.password):
            raise HTTPException(400, "Incorrect username or password")
        if not db_user.is_verified:
            raise HTTPException(400, "User not verified")
        return {"access_token": generate_access_token(db_user.id, secret=db_user.password)}

    @router.post("/logout", dependencies=[Depends(blacklist_access_token)])
    async def logout() -> DefaultResponse:
        return {"message": "User logged out"}

    @router.post("/verify/{verify_token}")
    async def verify(self, verify_user: VerifyUser) -> DefaultResponse:
        if verify_user.is_verified:
            raise HTTPException(400, "User already verified")
        verify_user.is_verified = True
        self.db.add(verify_user)
        await self.db.commit()
        return {"message": "User verified"}

    @router.post("/forgot-password", dependencies=[Depends(valid_turnstile_token)])
    async def forgot_password(self, email: EmailStr) -> DefaultResponse:
        statement = select(User).where(User.email == email)
        db_user = await self.db.exec(statement)
        db_user = db_user.first()
        if not db_user:
            raise HTTPException(404, "User not found")
        if not db_user.is_active:
            raise HTTPException(400, "User not active")
        send_email("", db_user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"username": db_user.username, "token": generate_verify_token(db_user.id, audience="reset_password")})
        return {"message": "Password reset email sent"}

    @router.post("/reset-password/{verify_token}")
    async def reset_password(self, verify_user: VerifyUser, password: str) -> DefaultResponse:
        verify_user.password = pwd_context.hash(password)
        self.db.add(verify_user)
        await self.db.commit()
        return {"message": "Password reset"}
