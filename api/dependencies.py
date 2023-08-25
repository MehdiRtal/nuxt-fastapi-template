from fastapi import Request
from fastapi.param_functions import Header
from fastapi.exceptions import HTTPException
import hmac
import hashlib
from typing import Annotated

from config import settings


async def verify_signature(request: Request, x_signature: Annotated[str, Header()]):
    return
    body = await request.body()
    signature = hmac.new(bytes(settings.SIGNATURE_SECRET), body, hashlib.sha512).hexdigest()
    if not hmac.compare_digest(signature, x_signature):
        raise HTTPException(403, "Invalid signature")