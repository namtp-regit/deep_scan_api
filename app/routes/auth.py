from fastapi import APIRouter

from app.requests.login_request import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(user: LoginRequest):
    return user


@router.post("/logout")
def logout(user_id: int):
    return True
