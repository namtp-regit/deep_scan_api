from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from core.cors import add_cors
from core.custom_openapi import custom_openapi
from core.exception_handlers import generic_exception_handler, http_exception_handler
from core.lifespan import lifespan
from core.validation_exception_handlers import validation_exception_handler
from app.middleware.http_logger import log_http_requests
from app.controllers import auth, items, users
from app.middleware.auth import AuthMiddleware


app = FastAPI(lifespan=lifespan)

# show authorize /docs
app.openapi = lambda: custom_openapi(app)


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
