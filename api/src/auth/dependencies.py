from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback

from src.users.models import User
from src.postgres import PostgresSession
from src.users.repository import UsersRepository
from src.redis_ import RedisSession

from src.auth.exceptions import PermissionRequired
from src.auth.service import AuthService
from src.auth.utils import google_oauth_client


def get_auth_service_session(postgres: PostgresSession, redis: RedisSession):
    users_repository = UsersRepository(postgres)
    return AuthService(users_repository, redis)

AuthServiceSession = Annotated[AuthService, Depends(get_auth_service_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

AccessToken = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(auth_service: AuthServiceSession, access_token: AccessToken):
    return await auth_service.get_current_user(access_token)

CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_verify_user(request: Request, auth_service: AuthServiceSession, verify_token: str):
    return await auth_service.get_verify_user(request, verify_token)

VerifyUser = Annotated[User, Depends(get_verify_user)]

async def require_superuser(current_user: CurrentUser):
    if not current_user.is_superuser:
        raise PermissionRequired

class CustomOAuth2AuthorizeCallback(OAuth2AuthorizeCallback):
    def __init__(self, client, route_name = None, redirect_url = None):
        self.client = client
        self.route_name = route_name
        self.redirect_url = redirect_url

    async def __call__(self, request: Request, code: str = None, code_verifier: str = None, state: str = None, error: str = None):
        if not code or error:
            raise HTTPException(400, error if error else None)
        if self.route_name:
            redirect_url = str(request.url_for(self.route_name))
        elif self.redirect_url:
            redirect_url = self.redirect_url
        else:
            redirect_url = str(request.url_for(request.scope["route"].name))
        access_token = await self.client.get_access_token(code, redirect_url, code_verifier)
        return access_token, state

google_oauth_callback = CustomOAuth2AuthorizeCallback(google_oauth_client)

GoogleOAuthCallback = Annotated[CustomOAuth2AuthorizeCallback, Depends(google_oauth_callback)]
