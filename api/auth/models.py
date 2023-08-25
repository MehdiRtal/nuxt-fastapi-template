from models import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"