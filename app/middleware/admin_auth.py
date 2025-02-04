from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from core.config import settings


class AdminAuthMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
        self.excluded_paths = [
            "/admin/docs",
            "/admin/openapi.json",
            "/admin/redoc",
            "/admin/login",
            "/admin/forgetPassword",
            "/admin/auth/login",
        ]

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive, send)

            # exclude url
            if request.url.path in self.excluded_paths:
                await self.app(scope, receive, send)
                return

            # check token
            authorization: str = request.headers.get("Authorization")
            if not authorization or not authorization.startswith("Bearer "):
                response = JSONResponse(
                    {"detail": "Unauthorized: Missing or invalid token"},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
                await response(scope, receive, send)
                return

            token = authorization.split(" ")[1]
            try:
                jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            except JWTError:
                response = JSONResponse(
                    {"detail": "Unauthorized: Invalid token"},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)
