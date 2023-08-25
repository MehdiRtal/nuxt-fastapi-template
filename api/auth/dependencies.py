from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
import requests
from typing import Annotated

from config import settings
from users.models import User
from database import Database
from redis import Redis

from .utils import oauth2_scheme


async def get_current_user(db: Database, redis: Redis, access_token: Annotated[str, Depends(oauth2_scheme)]):
    if await redis.sismember("invalid_access_tokens", access_token):
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

async def get_verify_user(request: Request, db: Database, verify_token: str):
    try:
        headers = jwt.get_unverified_header(verify_token)
        payload = jwt.decode(verify_token, settings.JWT_SECRET, algorithms=headers.get("alg"), audience=request.scope["route"].name)
    except JWTError:    
        raise HTTPException(401, "Invalid verify token")
    else:
        db_user = await db.get(User, payload.get("sub"))
        return db_user

VerifyUser = Annotated[User, Depends(get_verify_user)]

async def invalidate_access_token(redis: Redis, access_token: Annotated[str, Depends(oauth2_scheme)]):
    await redis.sadd("invalid_access_tokens", access_token)

def verify_turnstile_token(turnstile_token: str):
    return
    body = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": turnstile_token,
    }
    r = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", json=body)
    if not r.json()["success"]:
        raise HTTPException(403, "Invalid turnstile token")