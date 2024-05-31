from pydantic import PostgresDsn, RedisDsn, HttpUrl
from pydantic_settings import BaseSettings
import os
import pathlib
from enum import Enum


class Environment(str, Enum):
    PROD = "PROD"
    TEST = "TEST"
    DEV = "DEV"

    @property
    def is_prod(self):
        return self == self.PROD

    @property
    def is_test(self):
        return self == self.TEST

    @property
    def is_dev(self):
        return self == self.DEV

class Settings(BaseSettings):
    ENVIRONEMENT: Environment | None = None

    POSTGRES_URL: PostgresDsn

    REDIS_URL: RedisDsn

    ARQ_URL: RedisDsn

    LIMITER_URL: RedisDsn

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    VERIFY_TOKEN_EXPIRE_MINUTES: int

    JWT_SECRET: str
    JWT_ALGORITHM: str

    SENDGRID_API_KEY: str
    SENDGRID_EMAIL_FROM: str

    TURNSTILE_SECRET_KEY: str

    LOGFIRE_TOKEN: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    OTLP_COLLECTOR_URL: HttpUrl

environement = Environment(os.getenv("ENVIRONEMENT", Environment.DEV))
if environement.is_dev:
    settings = Settings(
        _env_file=(
            os.path.join(pathlib.Path(__file__).parent.parent, ".env"),
            os.path.join(pathlib.Path(__file__).parent.parent, ".dev.env")
        )
    )
elif environement.is_prod or environement.is_test:
    settings = Settings(
        _env_file=(
            os.path.join(pathlib.Path(__file__).parent.parent, ".env"),
            os.path.join(pathlib.Path(__file__).parent.parent, ".prod.env")
        )
    )
settings.ENVIRONEMENT = environement
