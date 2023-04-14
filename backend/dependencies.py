from fastapi import HTTPException, Cookie, Depends
from sqlmodel import select
from jose import jwt, JWTError
import requests
from typing import Annotated
from twilio.rest import Client

from config import settings
from models import *
from database import Session, get_session


def get_current_user(session_id: str = Cookie(None), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(session_id, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid session_id")
    else:
        db_user = session.get(User, payload["user_id"])
        return db_user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_verify_user(verification_sid: str, verification_code: str, session: Session = Depends(get_session)):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification_check = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verification_checks.create(verification_sid=verification_sid, code=verification_code)
    if verification_check.status != "approved":
        raise HTTPException(status_code=403, detail="Invalid verification code")
    statement = select(User).where(User.email == verification_check.to)
    db_user = session.exec(statement).first()
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
        raise HTTPException(status_code=403, detail="Invalid captcha token")