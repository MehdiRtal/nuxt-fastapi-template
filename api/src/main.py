from fastapi import FastAPI, Request, Depends, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
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
from src.utils import DefaultORJSONResponse, ORJSONResponse
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
    default_response_class=DefaultORJSONResponse,
    dependencies=[Depends(valid_signature), Depends(RateLimiter(times=100, minutes=1))],
    docs_url="/docs" if settings.ENVIRONEMENT.is_dev else None,
    redoc_url="/redoc" if settings.ENVIRONEMENT.is_dev else None
)

if settings.ENVIRONEMENT.is_prod:
    init_prometheus(app)

app.add_middleware(GZipMiddleware)

app.add_middleware(EventHandlerASGIMiddleware, handlers=[local_handler])

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exception: HTTPException):
    return ORJSONResponse({"status": "error", "message": exception.detail}, status_code=exception.status_code)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return ORJSONResponse({"status": "error", "message": exception.errors()}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

app.include_router(src.auth.router)
app.include_router(src.users.router)
app.include_router(src.items.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)
