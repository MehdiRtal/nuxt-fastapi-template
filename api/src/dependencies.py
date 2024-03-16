from fastapi import Request
from fastapi.param_functions import Header
from fastapi.exceptions import HTTPException
import hmac
import hashlib
from typing import Annotated
import httpx

from src.config import settings
from src.exceptions import InvalidSignature


async def valid_signature(request: Request, x_signature: Annotated[str, Header()] = None):
    if settings.ENVIRONEMENT.is_dev:
        return
    body = await request.body()
    signature = hmac.new(settings.SIGNATURE_SECRET.encode(), str(body).encode(), hashlib.sha512).hexdigest()
    if not hmac.compare_digest(signature, x_signature):
        raise InvalidSignature

def valid_turnstile_token(turnstile_token: str = None):
    if settings.ENVIRONEMENT.is_dev:
        return
    body = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": turnstile_token,
    }
    r = httpx.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", json=body)
    if not r.json()["success"]:
        raise HTTPException(403, "Invalid turnstile token")
