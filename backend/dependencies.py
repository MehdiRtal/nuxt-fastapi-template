from fastapi import HTTPException, Cookie, Depends
from jose import jwt, JWTError
import requests
from typing import Annotated

from config import settings
from models import *
from database import Session, get_session


def get_current_user(session_id: str = Cookie(default=None), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(session_id, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, audience="login")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        db_user = session.get(User, payload["user_id"])
        return db_user

CurrentUser = Annotated[User, Depends(get_current_user)]

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM, audience="token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    else:
        return payload["user_id"]

def verify_turnstile_token(turnstile_token: str = None):
    return
    body = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": turnstile_token,
    }
    r = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", json=body)
    if not r.json()["success"]:
        raise HTTPException(status_code=403, detail="Invalid captcha token")