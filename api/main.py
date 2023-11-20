from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.gzip import GZipMiddleware

from database import init_db
from cache import init_cache
from dependencies import valid_signature
import auth
import users
import items
from utils import CustomORJSONResponse, ORJSONResponse


app = FastAPI(title="API", default_response_class=CustomORJSONResponse, dependencies=[Depends(valid_signature)])

app.add_middleware(GZipMiddleware)

@app.on_event("startup")
async def startup():
    await init_db()
    init_cache()

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
