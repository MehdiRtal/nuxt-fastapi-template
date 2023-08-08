from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from contextlib import asynccontextmanager

from databases import init_db
from routers import auth, users, products, categories, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="API", version="1.0.0", lifespan=lifespan, default_response_class=ORJSONResponse)

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exception: HTTPException):
    return ORJSONResponse({"status": "error", "message": exception.detail}, status_code=exception.status_code)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return ORJSONResponse({"status": "error", "message": exception.errors()}, status_code=422)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(categories.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)