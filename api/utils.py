from fastapi.responses import ORJSONResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import settings


class CustomORJSONResponse(ORJSONResponse):
    def render(self, content):
        return super().render({"status": "success", **content})

def send_email(email_from: str, email_to: str, template_id: str, dynamic_template_data: dict = None):
    message = Mail(from_email=email_from, to_emails=email_to)
    message.template_id = template_id
    if dynamic_template_data:
        message.dynamic_template_data = dynamic_template_data
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
