from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr


from src.models import DefaultResponse
from src.users.models import User, UserCreate
from src.users.exceptions import UserAlreadyExists, UserNotVerified, UserNotActive, UserNotFound, UserAlreadyVerified, UserOAuthNotLinked
from src.db import DBSession

from src.auth.utils import generate_access_token, generate_verify_token, google_oauth_client, send_email, hash_password, verify_password
from src.auth.models import AccessToken
from src.auth.dependencies import VerifyUser, GoogleOAuthCallback
from src.auth.exceptions import InvalidCredentials


class AuthService:
    def __init__(self, db: DBSession | None = None):
        self.db = db

    async def register(self, user: UserCreate) -> DefaultResponse:
        try:
            user.password = hash_password(user.password)
            db_user = User(**user.model_dump())
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
        except IntegrityError:
            raise UserAlreadyExists()
        verify_token = generate_verify_token(db_user.id, audience="verify")
        send_email("", user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"full_name": user.full_name, "token": verify_token})
        return {"message": "Verification email sent"}

    async def verify(self, verify_user: VerifyUser) -> DefaultResponse:
        if verify_user.is_verified:
            raise UserAlreadyVerified()
        verify_user.is_verified = True
        self.db.add(verify_user)
        await self.db.commit()
        return {"message": "User verified"}

    async def login(self, form_data: OAuth2PasswordRequestForm) -> AccessToken:
        statement = select(User).where(User.email == form_data.username)
        db_user = await self.db.exec(statement)
        db_user = db_user.first()
        if not db_user or not verify_password(form_data.password, db_user.password):
            raise InvalidCredentials()
        if not db_user.is_verified:
            raise UserNotVerified()
        access_token = generate_access_token(db_user.id, secret=db_user.password)
        return {"access_token": access_token}

    async def sso_google(self, request: Request) -> dict:
        callback_url = request.url_for("sso_google_callback")
        authorization_url = await google_oauth_client.get_authorization_url(callback_url)
        return {"authorization_url": authorization_url}

    async def sso_google_callback(self, callback: GoogleOAuthCallback) -> AccessToken | dict:
        token, state = callback
        id, email = await google_oauth_client.get_id_email(token["access_token"])
        statement = select(User).where(User.email == email)
        db_user = await self.db.exec(statement)
        db_user = db_user.first()
        if db_user:
            if not db_user.google_oauth_refresh_token:
                raise UserOAuthNotLinked()
            db_user.google_oauth_refresh_token = token["refresh_token"]
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            access_token = generate_access_token(db_user.id, secret=db_user.password)
            return {"access_token": access_token}
        else:
            db_user = User(full_name="", email=email, password="", google_oauth_refresh_token=token["refresh_token"])
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            verify_token = generate_verify_token(db_user.id, audience="reset_password")
            return {"verify_token": verify_token}

    async def link_google(self, request: Request) -> dict:
        callback_url = request.url_for("link_google_callback")
        authorization_url = await google_oauth_client.get_authorization_url(callback_url)
        return {"authorization_url": authorization_url}

    async def link_google_callback(self, callback: GoogleOAuthCallback) -> DefaultResponse:
        token, state = callback
        id, email = await google_oauth_client.get_id_email(token["access_token"])
        statement = select(User).where(User.email == email)
        db_user = await self.db.exec(statement)
        db_user = db_user.first()
        if not db_user:
            raise UserNotFound()
        if not db_user.is_verified:
            raise UserNotVerified()
        if not db_user.is_active:
            raise UserNotActive()
        db_user.google_oauth_refresh_token = token["refresh_token"]
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return {"message": "Google OAuth linked"}

    async def logout(self) -> DefaultResponse:
        return {"message": "User logged out"}

    async def forgot_password(self, email: EmailStr) -> DefaultResponse:
        statement = select(User).where(User.email == email)
        db_user = await self.db.exec(statement)
        db_user = db_user.first()
        if not db_user:
            raise UserNotFound()
        if not db_user.is_active:
            raise UserNotActive()
        verify_token = generate_verify_token(db_user.id, audience="reset_password")
        send_email("", db_user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"full_name": db_user.full_name, "token": verify_token})
        return {"message": "Password reset email sent"}

    async def reset_password(self, verify_user: VerifyUser, password: str) -> DefaultResponse:
        verify_user.password = hash_password(password)
        self.db.add(verify_user)
        await self.db.commit()
        return {"message": "Password reset"}
