from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_jwt(payload: dict, audience: str = None, expiry_time: int = 30):
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=expiry_time)})
    if audience:
        payload.update({"aud": audience})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def send_email(email_from: str, email_to: str, template_id: str, dynamic_template_data: dict = {}):
    message = Mail(
        from_email=email_from,
        to_emails=email_to,
    )
    message.template_id = template_id
    message.dynamic_template_data = dynamic_template_data
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)