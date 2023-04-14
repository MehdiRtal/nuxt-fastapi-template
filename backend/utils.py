from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from twilio.rest import Client

from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_jwt(payload: dict, audience: str = None, expiry_time: int = 30):
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=expiry_time)})
    if audience:
        payload.update({"aud": audience})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def send_verify(email_to: str):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification = client.verify.v2.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(to=email_to, channel="email")
    return verification.sid