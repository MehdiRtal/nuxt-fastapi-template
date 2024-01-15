import sentry_sdk

from config import settings


def init_sentry():
    sentry_sdk.init(str(settings.SENTRY_DSN), enable_tracing=True)
