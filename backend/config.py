from pydantic import BaseSettings, EmailStr, PostgresDsn


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn

    JWT_SECRET : str
    JWT_ALGORITHM : str

    TWILIO_ACCOUNT_SID : str
    TWILIO_AUTH_TOKEN : str
    TWILIO_VERIFY_SERVICE_SID : str

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