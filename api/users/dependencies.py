from fastapi import Request
from fastapi.param_functions import Header
from fastapi.exceptions import HTTPException
import hmac
import hashlib
from typing import Annotated

from api.config import settings


async def valid_sellix_signature(request: Request, x_sellix_signature: Annotated[str, Header()] = None):
    return
    body = await request.body()
    signature = hmac.new(bytes(settings.SELLIX_SIGNATURE_SECRET), body, hashlib.sha512).hexdigest()
    if not hmac.compare_digest(signature, x_sellix_signature):
        raise HTTPException(403, "Invalid signature")
