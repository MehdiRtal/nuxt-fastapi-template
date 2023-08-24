from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn

    REDIS_URL: RedisDsn

    RQ_URL: RedisDsn

    ACCESS_TOKEN_EXPIRE_MINUTES : int

    VERIFY_TOKEN_EXPIRE_MINUTES : int

    JWT_SECRET : str
    JWT_ALGORITHM : str

    SIGNATURE_SECRET : str

    SENDGRID_API_KEY : str

    TURNSTILE_SECRET_KEY = str
    TURNSTILE_SITE_KEY = str

settings = Settings(_env_file="./.env")