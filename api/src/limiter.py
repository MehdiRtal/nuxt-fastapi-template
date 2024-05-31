from redis.asyncio.client import Redis
from fastapi_limiter import FastAPILimiter

from src.config import settings


limiter_connection = Redis.from_url(str(settings.LIMITER_URL))

async def init_limiter():
    await FastAPILimiter.init(limiter_connection)
