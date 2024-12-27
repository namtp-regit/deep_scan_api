from pathlib import Path
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.staticfiles import StaticFiles
from core.cors import add_cors
from core.custom_openapi import custom_openapi
from core.exception_handlers import (
    runtime_error_handler,
    generic_exception_handler,
    http_exception_handler,
)
from core.lifespan import lifespan
from core.validation_exception_handlers import validation_exception_handler
from app.middleware.http_logger import log_http_requests
from app.controllers import auth, uploads, users
from app.middleware.admin_auth import AdminAuthMiddleware

# make sure the 'public/uploads' directory exists
Path("public/uploads").mkdir(parents=True, exist_ok=True)

# main App
app = FastAPI(lifespan=lifespan)

# user sub-app
user_app = FastAPI(title="User API", version="1.0.0")

# admin sub-app
admin_app = FastAPI(title="Admin API", version="1.0.0")

# mount static files
app.mount("/public", StaticFiles(directory="public"), name="public")


# function to apply common settings
def configure_app(application: FastAPI):
    # add exception handlers
    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(Exception, generic_exception_handler)
    application.add_exception_handler(RuntimeError, runtime_error_handler)

    # add CORS middleware
    add_cors(application)

    # add logging middleware
    application.middleware("http")(log_http_requests)


# configure User App
configure_app(user_app)
user_app.include_router(auth.router)
user_app.include_router(uploads.router)
user_app.openapi = lambda: custom_openapi(app=user_app, prefix="/user")

# configure Admin App
configure_app(admin_app)
admin_app.include_router(auth.router)
admin_app.include_router(users.router)
admin_app.include_router(uploads.router)

# show authorize
admin_app.openapi = lambda: custom_openapi(app=admin_app, prefix="/admin")
admin_app.add_middleware(AdminAuthMiddleware)

# mount sub-apps to main app
app.mount("/user", user_app)
app.mount("/admin", admin_app)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Base!"}
