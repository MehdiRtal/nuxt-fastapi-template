from prometheus_fastapi_instrumentator import Instrumentator


def init_prometheus(app):
    Instrumentator().instrument(app).expose(app)
