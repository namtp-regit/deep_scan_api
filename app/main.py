from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.core.cors import add_cors
from app.core.exception_handlers import generic_exception_handler, http_exception_handler
from app.core.validation_exception_handlers import validation_exception_handler
from app.middleware.http_logger import log_http_requests
from app.routes import auth, items, users
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from app.database.connect import check_connection
from app.middleware.auth import AuthMiddleware


# check app startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not check_connection():
            raise SQLAlchemyError("Database connection failed during startup")
        print("Database connected successfully!")
    except Exception as e:
        print(f"Error during lifespan startup: {e}")
        raise e

    yield
    print("Application is shutting down...")


app = FastAPI(lifespan=lifespan)

# add custom message validation
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RequestValidationError, http_exception_handler)
app.add_exception_handler(RequestValidationError, generic_exception_handler)

# add cors middleware
add_cors(app)

# add logging middleware
app.middleware("http")(log_http_requests)

# middleware authentication
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Base!"}
