from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.requests.login_request import LoginRequest
from app.services import auth_service
from database.connect import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, request)


@router.post("/logout")
def logout(token: int):
    return auth_service.logout(token)
