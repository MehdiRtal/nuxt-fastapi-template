from fastapi import Depends
from redis.asyncio.client import Redis
from typing import Annotated

from src.config import settings


redis_connection = Redis.from_url(str(settings.REDIS_URL))

async def get_redis_session():
    async with redis_connection.client() as session:
        yield session

RedisSession = Annotated[Redis, Depends(get_redis_session)]
