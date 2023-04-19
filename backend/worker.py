from celery import Celery

from config import settings


app = Celery(__name__, backend=settings.CELERY_BACKEND_URL, broker=settings.CELERY_BROKER_URL, include=["tasks"])