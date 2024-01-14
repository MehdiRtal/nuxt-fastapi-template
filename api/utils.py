from fastapi.responses import ORJSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_cache import Coder
import orjson
from typing import Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sellix import Sellix

from config import settings


class CustomORJSONResponse(ORJSONResponse):
    def render(self, content):
        return super().render({"status": "success", **content})

class ORJSONCoder(Coder):
    @classmethod
    def encode(cls, value: Any) -> bytes:
        return orjson.dumps(value, default=jsonable_encoder, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY)

    @classmethod
    def decode(cls, value: bytes) -> Any:
        return orjson.loads(value)

def send_email(email_from: str, email_to: str, template_id: str, dynamic_template_data: dict = None):
    message = Mail(from_email=email_from, to_emails=email_to)
    message.template_id = template_id
    if dynamic_template_data:
        message.dynamic_template_data = dynamic_template_data
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)

def create_payment(value: float, email: str, custom_fields: dict, callback_url: str, **kwargs):
    client = Sellix(settings.SELLIX_API_KEY)
    payment_payload = {
        "value": value,
        "currency": "USD",
        "email": email,
        "custom_fields": custom_fields,
        "return_url": callback_url,
        **kwargs
    }
    payment = client.create_payment(**payment_payload)
    return payment["data"]["url"]
