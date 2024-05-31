from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from redis.asyncio.client import Redis

from src.config import settings


def send_email(email_to: str, template_id: str, dynamic_template_data: dict = None):
    message = Mail(from_email=settings.SENDGRID_EMAIL_FROM, to_emails=email_to)
    message.template_id = template_id
    if dynamic_template_data:
        message.dynamic_template_data = dynamic_template_data
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)

async def send_notification(redis: Redis, user_id: int, message: str):
    await redis.xadd(f"notifications:{user_id}", {"message": message})
