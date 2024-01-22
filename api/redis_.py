from fastapi import Depends
from redis.asyncio.client import Redis
from typing import Annotated

from .config import settings


connection = Redis.from_url(str(settings.REDIS_URL))

async def get_redis_session():
    async with connection.client() as session:
        yield session

RedisSession = Annotated[Redis, Depends(get_redis_session)]
