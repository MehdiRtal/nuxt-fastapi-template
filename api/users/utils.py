from sellix import Sellix

from config import settings


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
