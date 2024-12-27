from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI, prefix: str = ""):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Login using `mail_address` and `password` to get the token.",
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    openapi_schema["servers"] = [{"url": prefix}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema
