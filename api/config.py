from pydantic import PostgresDsn, RedisDsn, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn

    REDIS_URL: RedisDsn

    RQ_URL: RedisDsn

    CACHE_URL: RedisDsn

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    VERIFY_TOKEN_EXPIRE_MINUTES: int

    JWT_SECRET: str
    JWT_ALGORITHM: str

    SIGNATURE_SECRET: str

    SENTRY_DSN: HttpUrl

    SELLIX_API_KEY: str
    SELLIX_SIGNATURE_SECRET: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    SENDGRID_API_KEY: str

    TURNSTILE_SECRET_KEY: str
    TURNSTILE_SITE_KEY: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), ".env"))

settings = Settings()
