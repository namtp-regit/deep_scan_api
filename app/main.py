from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import auth, items, users
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from app.database.connect import check_connection
from app.middleware.auth import AuthMiddleware
from app.utils.status_code import VALIDATE_ERROR


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


# custom message validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = ".".join(map(str, error["loc"][1:]))
        msg = error["msg"]
        if field not in errors:
            errors[field] = []
        errors[field].append(msg)

    first_field = list(errors.keys())[0]
    first_message = errors[first_field][0]
    other_errors_count = len(errors) - 1
    suffix = (
        f" (and {other_errors_count} more error{'s' if other_errors_count > 1 else ''})"
        if other_errors_count > 0
        else ""
    )

    return JSONResponse(
        status_code=VALIDATE_ERROR,
        content={
            "message": f"{first_message}{suffix}",
            "errors": errors,
        },
    )


# middleware authentication
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Base!"}
