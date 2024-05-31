from redis.asyncio.connection import ConnectionPool
from arq.connections import ArqRedis

from src.config import settings
from src.logfire_ import init_logfire


arq_connection = ConnectionPool.from_url(str(settings.ARQ_URL))

arq = ArqRedis(pool_or_conn=arq_connection)

async def startup(ctx: dict):
    if settings.ENVIRONEMENT.is_prod:
        init_logfire("ARQ")

class WorkerSettings:
    redis_pool = arq
    on_startup = startup
    functions = []
