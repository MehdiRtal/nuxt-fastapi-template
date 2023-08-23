from fastapi import FastAPI, Request, Depends
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from contextlib import asynccontextmanager

from databases import init_db
from routers import auth, users
from dependencies import verify_signature


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

class CustomORJSONResponse(ORJSONResponse):
    def render(self, content):
        return super().render({"status": "success", **content})

app = FastAPI(title="API", lifespan=lifespan, default_response_class=ORJSONResponse, dependencies=[Depends(verify_signature)])

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exception: HTTPException):
    return ORJSONResponse({"status": "error", "message": exception.detail}, status_code=exception.status_code)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    return ORJSONResponse({"status": "error", "message": exception.errors()}, status_code=422)

app.include_router(auth.router)
app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, log_level="debug", reload=True)