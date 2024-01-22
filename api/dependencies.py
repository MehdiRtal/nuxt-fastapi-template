from fastapi import Request
from fastapi.param_functions import Header
from fastapi.exceptions import HTTPException
import hmac
import hashlib
from typing import Annotated
import httpx

from .config import settings


async def valid_signature(request: Request, x_signature: Annotated[str, Header()] = None):
    return
    body = await request.body()
    signature = hmac.new(bytes(settings.SIGNATURE_SECRET), body, hashlib.sha512).hexdigest()
    if not hmac.compare_digest(signature, x_signature):
        raise HTTPException(403, "Invalid signature")

def valid_turnstile_token(turnstile_token: str = None):
    return
    body = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": turnstile_token,
    }
    r = httpx.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", json=body)
    if not r.json()["success"]:
        raise HTTPException(403, "Invalid turnstile token")
