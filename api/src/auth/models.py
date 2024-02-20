from src.models import BaseModel


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
