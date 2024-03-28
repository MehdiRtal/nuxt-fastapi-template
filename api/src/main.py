from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_limiter.depends import RateLimiter
from contextlib import asynccontextmanager
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi_events.handlers.local import local_handler

from src.prometheus import init_prometheus
from src.postgres import init_postgres
from src.cache import init_cache
from src.limiter import init_limiter
from src.dependencies import valid_signature
from src.config import settings
import src.auth
import src.users
import src.items


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_postgres()
    init_cache()
    await init_limiter()
    yield

app = FastAPI(
    debug=True if settings.ENVIRONEMENT.is_dev else False,
    title="API",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    dependencies=[Depends(valid_signature), Depends(RateLimiter(times=100, minutes=1))],
    docs_url="/docs" if settings.ENVIRONEMENT.is_dev else None,
    redoc_url="/redoc" if settings.ENVIRONEMENT.is_dev else None
)

if settings.ENVIRONEMENT.is_prod:
    init_prometheus(app)

app.add_middleware(GZipMiddleware)

app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])

app.include_router(src.auth.router)
app.include_router(src.users.router)
app.include_router(src.items.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)
