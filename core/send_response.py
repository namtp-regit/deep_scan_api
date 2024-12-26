from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def send_response(code: int, message: str, data=None, errors=None):
    return JSONResponse(
        status_code=code,
        content={
            "status_code": code,
            "message": message,
            "errors": errors,
            "data": jsonable_encoder(data),
        },
    )


def raise_exception(code: int, message: str):
    response = send_response(code, message, data=None, errors={"detail": message})
    raise RuntimeError(response.body)
