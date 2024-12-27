from fastapi import Request
from core.logger import logger


async def log_http_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")

    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        try:
            body.decode("utf-8")
        except UnicodeDecodeError:
            logger.warning("Cannot decode body as UTF-8. It might be binary data.")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")
    logger.info(f"Response headers: {dict(response.headers)}")
    return response
