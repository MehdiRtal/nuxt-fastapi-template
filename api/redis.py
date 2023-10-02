from fastapi import Depends
from aioredis.client import Redis as RedisClient
from typing import Annotated

from config import settings


client = RedisClient.from_url(settings.REDIS_URL)

async def get_redis_session():
    redis = client
    async with redis.client() as session:
        yield session

Redis = Annotated[RedisClient, Depends(get_redis_session)]