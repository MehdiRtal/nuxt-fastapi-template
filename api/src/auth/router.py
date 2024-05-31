from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from fastapi_limiter.depends import RateLimiter
from typing import Annotated

from src.models import DefaultResponse
from src.users.models import UserCreatePublic
from src.dependencies import valid_turnstile_token

from src.auth.models import AccessToken, AuthorizationUrl, VerifyToken
from src.auth.dependencies import VerifyUser, AuthServiceSession, GoogleOAuthCallback


router = APIRouter(tags=["Authentication"], prefix="/auth")

@router.post("/register", status_code=201, dependencies=[Depends(valid_turnstile_token), Depends(RateLimiter(times=10, minutes=1))])
async def register(auth_service: AuthServiceSession, user: UserCreatePublic) -> DefaultResponse | VerifyToken:
    return await auth_service.register(user)

@router.post("/verify/{verify_token}")
async def verify(auth_service: AuthServiceSession, verify_user: VerifyUser) -> DefaultResponse:
    return await auth_service.verify(verify_user)

@router.post("/login", dependencies=[Depends(valid_turnstile_token), Depends(RateLimiter(times=10, minutes=1))])
async def login(auth_service: AuthServiceSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> AccessToken:
    return await auth_service.login(form_data)

@router.get("/link/google")
async def link_google(auth_service: AuthServiceSession, request: Request) -> AuthorizationUrl:
    return await auth_service.link_google(request)

@router.get("/link/google/callback")
async def link_google_callback(auth_service: AuthServiceSession, callback: GoogleOAuthCallback) -> DefaultResponse | AccessToken:
    return await auth_service.link_google_callback(callback)

@router.post("/logout")
async def logout(auth_service: AuthServiceSession) -> DefaultResponse:
    return await auth_service.logout()

@router.post("/forgot-password", dependencies=[Depends(valid_turnstile_token), Depends(RateLimiter(times=10, minutes=1))])
async def forgot_password(auth_service: AuthServiceSession, email: EmailStr) -> DefaultResponse | VerifyToken:
    return await auth_service.forgot_password(email)

@router.post("/reset-password/{verify_token}")
async def reset_password(auth_service: AuthServiceSession, verify_user: VerifyUser, password: str) -> DefaultResponse:
    return await auth_service.reset_password(verify_user, password)
