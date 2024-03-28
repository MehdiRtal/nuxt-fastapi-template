from redis.client import Redis
from rq import Queue
from rq_scheduler import Scheduler

from src.config import settings


connection = Redis.from_url(str(settings.RQ_URL))

queue = Queue(connection=connection)

scheduler = Scheduler(queue=queue, connection=connection)
