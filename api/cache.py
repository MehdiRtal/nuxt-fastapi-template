from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from utils import ORJSONCoder
from config import settings


connection = Redis.from_url(str(settings.CACHE_URL))

def init_cache():
    FastAPICache.init(RedisBackend(connection), coder=ORJSONCoder)
