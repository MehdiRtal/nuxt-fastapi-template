from sqlmodel import SQLModel
from pydantic import ConfigDict
import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default).decode()

class BaseModel(SQLModel):
    model_config = ConfigDict(json_loads=orjson.loads, json_dumps=orjson_dumps)


class DefaultResponse(BaseModel):
    message: str