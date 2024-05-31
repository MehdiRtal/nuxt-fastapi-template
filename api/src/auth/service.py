from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from redis.asyncio.client import Redis
from jose import JWTError, jwt

from src.users.models import User
from src.users.exceptions import UserAlreadyExists, UserNotVerified, UserNotActive, UserAlreadyVerified
from src.users.repository import UsersRepository
from src.config import settings
from src.utils import send_email

from src.auth.utils import generate_access_token, generate_verify_token, hash_password, verify_password, verify_access_token, verify_verify_token, google_oauth_client
from src.auth.exceptions import InvalidCredentials, InvalidAccessToken, InvalidVerifyToken


class AuthService:
    def __init__(self, users_repository: UsersRepository, redis: Redis):
        self.users_repository = users_repository
        self.redis = redis

    async def get_current_user(self, access_token: str):
        if await self.redis.sismember("blacklisted_access_tokens", access_token):
            raise InvalidAccessToken
        try:
            payload = jwt.get_unverified_claims(access_token)
            user_id = int(payload.get("sub"))
            db_user = await self.users_repository.get_by_id(user_id)
            verify_access_token(access_token, db_user.password)
        except JWTError:
            raise InvalidAccessToken
        else:
            if not db_user.is_active:
                raise UserNotActive
            return db_user

    async def get_verify_user(self, request: Request, verify_token: str):
        try:
            payload = verify_verify_token(verify_token, request.scope["route"].name)
        except JWTError:
            raise InvalidVerifyToken
        else:
            user_id = int(payload.get("sub"))
            db_user = await self.users_repository.get_by_id(user_id)
            return db_user

    async def register(self, user: User):
        user.password = hash_password(user.password)
        db_user = await self.users_repository.add(user)
        if not db_user:
            raise UserAlreadyExists
        verify_token = generate_verify_token(db_user.id, audience="verify")
        send_email(user.email, "d-8ff0eab7a43c4c6d906e50c402f9abca", {"fullName": user.full_name, "verifyToken": verify_token})
        if settings.ENVIRONEMENT.is_test:
            return {"verify_token": verify_token}
        else:
            return {"detail": "Verification email sent"}

    async def verify(self, verify_user: User):
        if verify_user.is_verified:
            raise UserAlreadyVerified
        verify_user.is_verified = True
        await self.users_repository.update(verify_user)
        send_email(verify_user.email, "d-8ff0eab7a43c4c6d906e50c402f9abca", {"fullName": verify_user.full_name})
        return {"detail": "User verified"}

    async def login(self, form_data: OAuth2PasswordRequestForm):
        db_user = await self.users_repository.get_by_email(form_data.username)
        if not db_user:
            raise InvalidCredentials
        if not verify_password(form_data.password, db_user.password):
            raise InvalidCredentials
        if not db_user.is_verified:
            raise UserNotVerified
        access_token = generate_access_token(db_user.id, secret=db_user.password)
        return {"access_token": access_token}

    async def link_google(self, request: Request):
        callback_url = request.url_for("link_google_callback")
        authorization_url = await google_oauth_client.get_authorization_url(callback_url)
        return {"authorization_url": authorization_url}

    async def link_google_callback(self, callback):
        token, state = callback
        email = await google_oauth_client.get_email(token["access_token"])
        db_user = await self.users_repository.get_by_email(email)
        if not db_user.is_verified:
            raise UserNotVerified
        if not db_user.is_active:
            raise UserNotActive
        db_user.google_oauth_refresh_token = token["refresh_token"]
        db_user = await self.users_repository.update(db_user)
        return {"detail": "google OAuth linked"}

    async def logout(self, access_token: str):
        await self.redis.sadd("blacklisted_access_tokens", access_token)
        return {"detail": "User logged out"}

    async def forgot_password(self, email: EmailStr):
        db_user = await self.users_repository.get_by_email(email)
        if not db_user.is_active:
            raise UserNotActive
        verify_token = generate_verify_token(db_user.id, audience="reset_password")
        send_email(db_user.email, "d-8ff0eab7a43c4c6d906e50c402f9abca", {"fullName": db_user.full_name, "verifyToken": verify_token})
        if settings.ENVIRONEMENT.is_test:
            return {"verify_token": verify_token}
        else:
            return {"detail": "Password reset email sent"}

    async def reset_password(self, verify_user: User, password: str):
        verify_user.password = hash_password(password)
        verify_user = await self.users_repository.update(verify_user)
        send_email(verify_user.email, "d-8ff0eab7a43c4c6d906e50c402f9abca", {"fullName": verify_user.full_name})
        return {"detail": "Password reset"}
