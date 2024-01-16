from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from authlib.integrations.starlette_client import OAuth

from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth = OAuth()

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    scope="openid profile email",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET
)

def generate_jwt(payload: dict, secret: str, expire_minutes: int, audience: str = None):
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=expire_minutes)})
    if audience:
        payload.update({"aud": audience})
    return jwt.encode(payload, secret, algorithm=settings.JWT_ALGORITHM)

def generate_access_token(user_id: int, secret: str):
    return generate_jwt({"sub": user_id}, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES, secret=secret)

def generate_verify_token(user_id: int, audience: str):
    return generate_jwt({"sub": user_id}, secret=settings.JWT_SECRET, expire_minutes=settings.VERIFY_TOKEN_EXPIRE_MINUTES, audience=audience)
