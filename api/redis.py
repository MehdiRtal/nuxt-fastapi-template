from fastapi import Depends
import aioredis
from aioredis import Redis as Session
from typing import Annotated

from config import settings


async def get_redis():
    redis = aioredis.from_url(settings.REDIS_URL)
    async with redis.client() as session:
        yield session

Redis = Annotated[Session, Depends(get_redis)]