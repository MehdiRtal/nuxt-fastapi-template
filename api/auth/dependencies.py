from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from typing import Annotated
from httpx_oauth.integrations.fastapi import OAuth2AuthorizeCallback

from config import settings
from users.models import User
from db import DBSession
from redis_ import RedisSession

from .utils import oauth2_scheme, google_oauth_client


AccessToken = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(db: DBSession, redis: RedisSession, access_token: AccessToken):
    if await redis.sismember("blacklisted_access_tokens", access_token):
        raise HTTPException(401, "Invalid access token")
    try:
        headers = jwt.get_unverified_header(access_token)
        payload = jwt.get_unverified_claims(access_token)
        db_user = await db.get(User, payload.get("sub"))
        jwt.decode(access_token, db_user.password, algorithms=headers.get("alg"))
    except JWTError:
        raise HTTPException(401, "Invalid access token")
    else:
        if not db_user.is_active:
            raise HTTPException(400, "User not active")
        return db_user

CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_verify_user(request: Request, db: DBSession, verify_token: str):
    try:
        headers = jwt.get_unverified_header(verify_token)
        payload = jwt.decode(verify_token, settings.JWT_SECRET, algorithms=headers.get("alg"), audience=request.scope["route"].name)
    except JWTError:
        raise HTTPException(401, "Invalid verify token")
    else:
        db_user = await db.get(User, payload.get("sub"))
        return db_user

VerifyUser = Annotated[User, Depends(get_verify_user)]

async def require_superuser(current_user: CurrentUser):
    if not current_user.is_superuser:
        raise HTTPException(401, "User does not have required permissions")

async def blacklist_access_token(redis: RedisSession, access_token: AccessToken):
    await redis.sadd("blacklisted_access_tokens", access_token)

class CustomOAuth2AuthorizeCallback(OAuth2AuthorizeCallback):
    def __init__(self, client, route_name = None, redirect_url = None):
        self.client = client
        self.route_name = route_name
        self.redirect_url = redirect_url

    async def __call__(self, request: Request, code: str = None, code_verifier: str = None, state: str = None, error: str = None):
        if code is None or error is not None:
            raise HTTPException(400, error if error is not None else None)
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
