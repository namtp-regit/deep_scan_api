from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.requests.login_request import LoginRequest
from app.services.auth_service import AuthService
from database.connect import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(session: Session = Depends(get_db)) -> AuthService:
    return AuthService(session)


@router.post("/login")
def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login(request)


@router.post("/logout")
def logout(token: int, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.logout(token)
