from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from utils.status_code import VALIDATE_ERROR


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
