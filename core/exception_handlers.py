import json
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred."},
    )


async def runtime_error_handler(request: Request, exc: RuntimeError):
    try:
        response_data = json.loads(exc.args[0])
    except Exception:
        response_data = {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error",
            "errors": {"detail": "An unexpected error occurred."},
            "data": None,
        }

    return JSONResponse(
        status_code=response_data["status_code"],
        content=response_data,
    )
