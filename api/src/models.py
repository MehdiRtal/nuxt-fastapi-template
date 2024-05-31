from sqlmodel import SQLModel


class BaseModel(SQLModel):
    pass

class DefaultResponse(BaseModel):
    detail: str

class HealthCheck(BaseModel):
    status: str = "ok"
