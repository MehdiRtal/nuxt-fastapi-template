import bcrypt
from jose import jwt
import datetime
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2
from httpx_oauth.errors import GetIdEmailError

from src.config import settings

class AppleOAuth2(OAuth2):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        scopes: list[str] = ["name", "email"],
        name="apple",
    ):
        super().__init__(
            client_id,
            client_secret,
            "https://appleid.apple.com/auth/authorize",
            "https://appleid.apple.com/auth/token",
            "https://appleid.apple.com/auth/revoke",
            name=name,
            base_scopes=scopes,
        )

    async def get_id_email(self, token: str) -> tuple:
        async with self.get_httpx_client() as client:
            response = await client.post(
                "https://appleid.apple.com/auth/keys",
                headers={**self.request_headers, "Authorization": f"Bearer {token}"},
            )
            if response.status_code >= 400:
                raise GetIdEmailError(response.json())
            data= response.json()
            user_id = data.get("sub", "")
            user_email = data.get("email", None)
            return user_id, user_email

apple_oauth_client = AppleOAuth2(settings.APPLE_CLIENT_ID, settings.APPLE_CLIENT_SECRET)

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
