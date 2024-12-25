from fastapi import Request
from fastapi.responses import JSONResponse
from utils.status_code import SERVER_ERROR
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=SERVER_ERROR,
        content={"message": "An unexpected error occurred."},
    )
