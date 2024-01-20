from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from contextlib import asynccontextmanager

from sentry import init_sentry
from db import init_db
from cache import init_cache
from dependencies import valid_signature
from utils import DefaultORJSONResponse, ORJSONResponse
from config import settings
import auth
import users
import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    init_cache()
    if settings.ENVIRONEMENT.is_prod:
        init_sentry()
    yield

app = FastAPI(
    title="API",
    lifespan=lifespan,
    default_response_class=DefaultORJSONResponse,
    dependencies=[Depends(valid_signature)],
    docs_url="/docs" if settings.ENVIRONEMENT.is_dev else None,
    redoc_url="/redoc" if settings.ENVIRONEMENT.is_dev else None
)

app.add_middleware(GZipMiddleware)

if settings.ENVIRONEMENT.is_dev:
    app.add_middleware(ServerErrorMiddleware, debug=True)

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exception: HTTPException):
    return ORJSONResponse({"status": "error", "message": exception.detail}, status_code=exception.status_code)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return ORJSONResponse({"status": "error", "message": exception.errors()}, status_code=422)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        log_level="debug",
        reload=True
    )
