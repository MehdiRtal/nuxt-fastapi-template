from fastapi import FastAPI
from prometheus_fastapi_instrumentator.instrumentation import PrometheusFastApiInstrumentator


prometheus = PrometheusFastApiInstrumentator()

def init_prometheus(app: FastAPI):
    prometheus.instrument(app).expose(app)
