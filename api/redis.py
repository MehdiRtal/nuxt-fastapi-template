from fastapi import Depends
import aioredis
from aioredis import Redis as Session
from typing import Annotated

from config import settings


async def get_redis_session():
    redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    async with redis.client() as session:
        yield session

Redis = Annotated[Session, Depends(get_redis_session)]