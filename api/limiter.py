from redis.asyncio.client import Redis
from fastapi_limiter import FastAPILimiter

from api.config import settings


connection = Redis.from_url(str(settings.LIMITER_URL))

async def init_limiter():
    await FastAPILimiter.init(connection)
