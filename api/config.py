from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: PostgresDsn

    RQ_URL: RedisDsn

    JWT_SECRET : str
    JWT_ALGORITHM : str

    SENDGRID_API_KEY : str

    TURNSTILE_SECRET_KEY = str
    TURNSTILE_SITE_KEY = str

settings = Settings(_env_file="./.env")