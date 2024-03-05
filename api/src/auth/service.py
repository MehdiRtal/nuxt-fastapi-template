from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from src.models import DefaultResponse
from src.users.models import User, UserCreate
from src.users.exceptions import UserAlreadyExists, UserNotVerified, UserNotActive, UserNotFound, UserAlreadyVerified, UserOAuthNotLinked
from src.exceptions import EntityAlreadyExists
from src.users.repository import UsersRepository

from src.auth.utils import generate_access_token, generate_verify_token, google_oauth_client, send_email, hash_password, verify_password
from src.auth.models import AccessToken
from src.auth.exceptions import InvalidCredentials


class AuthService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def register(self, user: UserCreate) -> DefaultResponse:
        try:
            user.password = hash_password(user.password)
            db_user = await self.users_repository.add(user)
        except EntityAlreadyExists:
            raise UserAlreadyExists()
        verify_token = generate_verify_token(db_user.id, audience="verify")
        send_email("", user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"full_name": user.full_name, "token": verify_token})
        return {"message": "Verification email sent"}

    async def verify(self, verify_user: User) -> DefaultResponse:
        if verify_user.is_verified:
            raise UserAlreadyVerified()
        verify_user.is_verified = True
        await self.users_repository.update(verify_user)
        return {"message": "User verified"}

    async def login(self, form_data: OAuth2PasswordRequestForm) -> AccessToken:
        db_user = await self.users_repository.get_by_email(form_data.username)
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

    async def sso_google_callback(self, callback) -> AccessToken | dict:
        token, state = callback
        id, email = await google_oauth_client.get_id_email(token["access_token"])
        db_user = await self.users_repository.get_by_email(email)
        if db_user:
            if not db_user.google_oauth_refresh_token:
                raise UserOAuthNotLinked()
            db_user.google_oauth_refresh_token = token["refresh_token"]
            db_user = await self.users_repository.update(db_user)
            access_token = generate_access_token(db_user.id, secret=db_user.password)
            return {"access_token": access_token}
        else:
            db_user = User(full_name="", email=email, password="", google_oauth_refresh_token=token["refresh_token"])
            db_user = await self.users_repository.update(db_user)
            verify_token = generate_verify_token(db_user.id, audience="reset_password")
            return {"verify_token": verify_token}

    async def link_google(self, request: Request) -> dict:
        callback_url = request.url_for("link_google_callback")
        authorization_url = await google_oauth_client.get_authorization_url(callback_url)
        return {"authorization_url": authorization_url}

    async def link_google_callback(self, callback) -> DefaultResponse:
        token, state = callback
        id, email = await google_oauth_client.get_id_email(token["access_token"])
        db_user = await self.users_repository.get_by_email(email)
        if not db_user:
            raise UserNotFound()
        if not db_user.is_verified:
            raise UserNotVerified()
        if not db_user.is_active:
            raise UserNotActive()
        db_user.google_oauth_refresh_token = token["refresh_token"]
        db_user = await self.users_repository.update(db_user)
        return {"message": "Google OAuth linked"}

    async def logout(self) -> DefaultResponse:
        return {"message": "User logged out"}

    async def forgot_password(self, email: EmailStr) -> DefaultResponse:
        db_user = await self.users_repository.get_by_email(email)
        if not db_user:
            raise UserNotFound()
        if not db_user.is_active:
            raise UserNotActive()
        verify_token = generate_verify_token(db_user.id, audience="reset_password")
        send_email("", db_user.email, "d-9b9b2f1b5b4a4b8e9b9b2f1b5b4b8e9b", {"full_name": db_user.full_name, "token": verify_token})
        return {"message": "Password reset email sent"}

    async def reset_password(self, verify_user: User, password: str) -> DefaultResponse:
        verify_user.password = hash_password(password)
        verify_user = await self.users_repository.update(verify_user)
        return {"message": "Password reset"}
