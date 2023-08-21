from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_restful.cbv import cbv
from sqlmodel import select, or_
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from typing import Annotated

from models import User, UserCreate, Token, BaseModel
from databases import Database
from dependencies import VerifyUser, verify_turnstile_token
from utils import pwd_context, generate_access_token, generate_verify_token
from tasks import send_email
from queues import low_queue


router = APIRouter(tags=["Authentication"], prefix="/auth")

@cbv(router)
class Auth:
    db: Database

    @router.post("/register", status_code=201, dependencies=[Depends(verify_turnstile_token)])
    def register(self, user: UserCreate) -> BaseModel:
        try:
            user.password = pwd_context.hash(user.password)
            db_user = User(**user.model_dump())
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            raise HTTPException(400, "Username or email already in use")
        low_queue.enqueue(send_email, "", user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"username": user.username, "token": generate_verify_token(db_user.id, audience="verify")})
        return {"message": "Verification email sent"}

    @router.post("/login", dependencies=[Depends(verify_turnstile_token)])
    def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
        statement = select(User).where(or_(User.username == form_data.username, User.email == form_data.username))
        db_user = self.db.exec(statement).first()
        if not db_user or not pwd_context.verify(form_data.password, db_user.password):
            raise HTTPException(400, "Incorrect username or password")
        if not db_user.is_verified:
            raise HTTPException(400, "User not verified")
        return {"access_token": generate_access_token(db_user.id, secret=db_user.password)}

    @router.post("/logout")
    def logout():
        return {"message": "User logged out"}

    @router.post("/verify/{verify_token}")
    def verify(self, verify_user: VerifyUser) -> BaseModel:
        if verify_user.is_verified:
            raise HTTPException(400, "User already verified")
        verify_user.is_verified = True
        self.db.add(verify_user)
        self.db.commit()
        return {"message": "User verified"}

    @router.post("/forgot-password", dependencies=[Depends(verify_turnstile_token)])
    def forgot_password(self, email: EmailStr) -> BaseModel:
        statement = select(User).where(User.email == email)
        db_user = self.db.exec(statement).first()
        if not db_user:
            raise HTTPException(404, "User not found")
        if not db_user.is_active:
            raise HTTPException(400, "User not active")
        low_queue.enqueue(send_email, "", db_user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"username": db_user.username, "token": generate_verify_token(db_user.id, audience="reset_password")})
        return {"message": "Password reset email sent"}

    @router.post("/reset-password/{verify_token}")
    def reset_password(self, verify_user: VerifyUser, password: str) -> BaseModel:
        verify_user.password = pwd_context.hash(password)
        self.db.add(verify_user)
        self.db.commit()
        return {"message": "Password reset"}