from sqlmodel import SQLModel


class BaseModel(SQLModel):
    pass

class DefaultResponse(BaseModel):
    detail: str
