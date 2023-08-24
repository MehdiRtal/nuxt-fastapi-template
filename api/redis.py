import aioredis

from config import settings


redis = aioredis.from_url(settings.REDIS_URL)