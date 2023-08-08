from redis import Redis
from rq import Queue


low_queue = Queue(name="low", connection=Redis())

medium_queue = Queue(name="medium", connection=Redis())

high_queue = Queue(name="high", connection=Redis())