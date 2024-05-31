from fastapi.exceptions import HTTPException
import httpx

from src.config import settings


async def valid_turnstile_token(turnstile_token: str = None):
    return
    if settings.ENVIRONEMENT.is_dev:
        return
    body = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": turnstile_token
    }
    async with httpx.AsyncClient() as client:
        r = await client.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", json=body)
        if not r.json()["success"]:
            raise HTTPException(403, "Invalid turnstile token")
