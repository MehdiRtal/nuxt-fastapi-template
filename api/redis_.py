from fastapi import Depends
from redis.asyncio.client import Redis as Redis_
from typing import Annotated

from config import settings


connection = Redis_.from_url(str(settings.REDIS_URL))

async def get_redis_session():
    async with connection.client() as session:
        yield session

RedisSession = Annotated[Redis_, Depends(get_redis_session)]
