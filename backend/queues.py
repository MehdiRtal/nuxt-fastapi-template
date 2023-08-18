import redis
from rq import Queue

from config import settings


connection = redis.from_url(settings.RQ_URL)

low_queue = Queue(name="low", connection=connection)

medium_queue = Queue(name="medium", connection=connection)

high_queue = Queue(name="high", connection=connection)