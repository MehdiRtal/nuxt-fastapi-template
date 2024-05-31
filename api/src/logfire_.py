from fastapi import FastAPI, Request, Response
import logfire
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry import trace
from loguru import logger
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

from src.config import settings
from src.postgres import postgres_engine


class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        span = trace.get_current_span()
        trace_id_hex = span.get_span_context().trace_id
        trace_id = format(trace_id_hex, "032x")
        response.headers["X-Trace-Id"] = trace_id
        return response

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/metrics":
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
        response = await call_next(request)
        return response

def init_logfire(service_name: str, app: FastAPI = None):
    otlp_exporter = OTLPSpanExporter(str(settings.OTLP_COLLECTOR_URL))
    span_processor = BatchSpanProcessor(otlp_exporter)
    metric_reader = PrometheusMetricReader()
    logfire.configure(
        token=settings.LOGFIRE_TOKEN,
        service_name=service_name,
        processors=[span_processor],
        metric_readers=[metric_reader],
        collect_system_metrics=True
    )
    logger.configure(handlers=[logfire.loguru_handler()])
    logfire.instrument_httpx()
    SQLAlchemyInstrumentor().instrument(engine=postgres_engine.sync_engine)
    RedisInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    if app:
        app.add_middleware(TraceIDMiddleware)
        logfire.instrument_fastapi(app)
        app.add_middleware(PrometheusMiddleware)
