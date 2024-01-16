from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from sentry import init_sentry
from starlette.middleware.sessions import SessionMiddleware

from database import init_db
from cache import init_cache
from dependencies import valid_signature
import auth
import users
import items
from utils import CustomORJSONResponse, ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    init_cache()
    init_sentry()
    yield

app = FastAPI(title="API", lifespan=lifespan, default_response_class=CustomORJSONResponse, dependencies=[Depends(valid_signature)])

app.add_middleware(GZipMiddleware)
app.add_middleware(SessionMiddleware, secret_key="secret")

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
    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)
