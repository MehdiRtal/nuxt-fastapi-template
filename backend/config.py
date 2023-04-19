from pydantic import BaseSettings, EmailStr, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn

    CELERY_BROKER_URL: RedisDsn
    CELERY_BACKEND_URL: RedisDsn

    JWT_SECRET : str
    JWT_ALGORITHM : str

    SENDGRID_API_KEY : str

    TURNSTILE_SECRET_KEY = str
    TURNSTILE_SITE_KEY = str

    # EMAIL_HOST = str
    # EMAIL_PORT = int
    # EMAIL_USERNAME = str
    # EMAIL_PASSWORD = str
    # EMAIL_FROM = EmailStr

    class Config:
        env_file = ".env"

settings = Settings()