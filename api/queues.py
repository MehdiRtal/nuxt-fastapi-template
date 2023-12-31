from redis.client import Redis
from rq import Queue

from config import settings


connection = Redis.from_url(str(settings.RQ_URL))

low_queue = Queue(name="low", connection=connection)

medium_queue = Queue(name="medium", connection=connection)

high_queue = Queue(name="high", connection=connection)
