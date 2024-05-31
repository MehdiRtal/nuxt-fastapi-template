from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import os
import pathlib
import json

from src.postgres import init_postgres
from src.limiter import init_limiter
from src.logfire_ import init_logfire
from src.config import settings
from src.models import HealthCheck
import src.auth.router as auth
import src.users.router as users

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_postgres()
    await init_limiter()
    yield

app = FastAPI(
    debug=True if settings.ENVIRONEMENT.is_dev else False,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    docs_url="/docs" if settings.ENVIRONEMENT.is_dev else None,
    redoc_url="/redoc" if settings.ENVIRONEMENT.is_dev else None
)

if settings.ENVIRONEMENT.is_prod:
    init_logfire("API", app=app)

app.add_middleware(GZipMiddleware)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health")
def health_check() -> HealthCheck:
    return {"status": "ok"}

if settings.ENVIRONEMENT.is_dev:
    with open(os.path.join(pathlib.Path(__file__).parent.parent, "openapi.json"), "w") as f:
        json.dump(app.openapi(), f, indent=4)
