from fastapi import Request, Depends
from fastapi.param_functions import Header
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
import hmac
import hashlib
import requests
from typing import Annotated

from config import settings
from models import User
from databases import Database
from utils import oauth2_scheme


def get_current_user(db: Database, access_token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.get_unverified_header(access_token)
        db_user = db.get(User, payload.get("sub"))
        jwt.decode(access_token, db_user.password, algorithms=settings.JWT_ALGORITHM)
    except JWTError:
        raise HTTPException(401, "Invalid access token")
    else:
        if not db_user.is_active:
            raise HTTPException(400, "User not active")
        return db_user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_verify_user(db: Database, request: Request, verify_token: str):
    try:
        payload = jwt.decode(verify_token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, audience=request.scope["route"].name)
    except JWTError:    
        raise HTTPException(401, "Invalid verify token")
    else:
        db_user = db.get(User, payload.get("sub"))
        return db_user

VerifyUser = Annotated[User, Depends(get_verify_user)]

def verify_turnstile_token(turnstile_token: str):
    return
    body = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": turnstile_token,
    }
    r = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", json=body)
    if not r.json()["success"]:
        raise HTTPException(403, "Invalid turnstile token")
    
async def verify_api_signature(request: Request, x_api_signature: Annotated[str, Header()]):
    return
    body = await request.body()
    signature = hmac.new(settings.API_SIGNATURE_SECRET, body, hashlib.sha512).hexdigest()
    if not hmac.compare_digest(signature, x_api_signature):
        raise HTTPException(403, "Invalid API signature")