import sentry_sdk

from api.config import settings


def init_sentry():
    sentry_sdk.init(str(settings.SENTRY_DSN), enable_tracing=True)
