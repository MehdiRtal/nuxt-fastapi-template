from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_jwt(payload: dict, secret: str = settings.JWT_SECRET, audience: str = None, expiry_time: int = 30):
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=expiry_time)})
    if audience:
        payload.update({"aud": audience})
    return jwt.encode(payload, secret, algorithm=settings.JWT_ALGORITHM)