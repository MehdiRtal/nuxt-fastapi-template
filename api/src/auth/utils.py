import bcrypt
from jose import jwt
import datetime
from httpx_oauth.clients.google import GoogleOAuth2

from src.config import settings


google_oauth_client = GoogleOAuth2(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET)

def hash_password(password: str):
    pwd_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt).decode()
    return hashed_password

def verify_password(plain_password: str, hashed_password: str):
    plain_pwd_bytes = plain_password.encode()
    hashed_pwd_bytes = hashed_password.encode()
    return bcrypt.checkpw(plain_pwd_bytes, hashed_pwd_bytes)

def generate_jwt(payload: dict, secret: str, expire_minutes: int, audience: str = None):
    payload.update({"exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expire_minutes)})
    if audience:
        payload.update({"aud": audience})
    return jwt.encode(payload, secret, algorithm=settings.JWT_ALGORITHM)

def generate_access_token(user_id: int, secret: str):
    return generate_jwt({"sub": str(user_id)}, secret=secret, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

def generate_verify_token(user_id: int, audience: str):
    return generate_jwt({"sub": str(user_id)}, secret=settings.JWT_SECRET, expire_minutes=settings.VERIFY_TOKEN_EXPIRE_MINUTES, audience=audience)

def verify_jwt(token: str, secret: str, audience: str = None):
    return jwt.decode(token, secret, algorithms=settings.JWT_ALGORITHM, audience=audience)

def verify_access_token(access_token: str, secret: str):
    return verify_jwt(token=access_token, secret=secret)

def verify_verify_token(verify_token: str, audience: str):
    return verify_jwt(token=verify_token, secret=settings.JWT_SECRET, audience=audience)
