from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
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
        raise HTTPException(status_code=401, detail="Invalid access token")
    else:
        if not db_user.is_active:
            raise HTTPException(status_code=400, detail="User not active")
        return db_user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_verify_user(db: Database, request: Request, verify_token: str):
    try:
        payload = jwt.decode(verify_token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, audience=request.scope["route"].name)
    except JWTError:    
        raise HTTPException(status_code=401, detail="Invalid verify token")
    else:
        db_user = db.get(User, payload.get("sub"))
        return db_user

VerifyUser = Annotated[User, Depends(get_verify_user)]

def verify_turnstile_token(turnstile_token: str = None):
    return
    body = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": turnstile_token,
    }
    r = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", json=body)
    if not r.json()["success"]:
        raise HTTPException(status_code=403, detail="Invalid turnstile token")