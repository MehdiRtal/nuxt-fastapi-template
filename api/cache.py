from redis.client import Redis
from typing import Any
import orjson
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.encoders import jsonable_encoder
from fastapi_cache import Coder

from config import settings


connection = Redis.from_url(str(settings.CACHE_URL))

class ORJSONCoder(Coder):
    @classmethod
    def encode(cls, value: Any) -> bytes:
        return orjson.dumps(value, default=jsonable_encoder, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY)

    @classmethod
    def decode(cls, value: bytes) -> Any:
        return orjson.loads(value)

def init_cache():
    FastAPICache.init(RedisBackend(connection), coder=ORJSONCoder)
