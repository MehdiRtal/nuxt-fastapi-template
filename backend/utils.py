from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_jwt(payload: dict, audience: str = None, expiry_time: int = 30):
    payload.update({"exp": datetime.utcnow() + timedelta(minutes=expiry_time)})
    if audience:
        payload.update({"aud": audience})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def send_email(email_to: str, subject: str, template: str, context: dict):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True, auto_reload=False)
    body = MIMEText(env.get_template(template).render(context), "html")
    message.attach(body)
    with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=ssl.create_default_context()) as server:
        server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, email_to, message.as_string())