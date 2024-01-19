from redis.asyncio.client import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.encoders import jsonable_encoder
from fastapi_cache import Coder
import orjson

from config import settings


class ORJSONCoder(Coder):
    @classmethod
    def encode(cls, value):
        return orjson.dumps(value, default=jsonable_encoder, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY)

    @classmethod
    def decode(cls, value):
        return orjson.loads(value)

connection = Redis.from_url(str(settings.CACHE_URL))

def init_cache():
    FastAPICache.init(RedisBackend(connection), coder=ORJSONCoder)
