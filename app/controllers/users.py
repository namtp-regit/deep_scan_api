from fastapi import APIRouter, Depends, status
from app.requests.param_request import RequestModel
from app.requests.user_request import CreateUserRequest, UpdateUserRequest
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from core.extract_request_params import extract_request_params
from core.send_response import send_response
from database.connect import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return UserService.get_users(db)


@router.get("/list")
def list(request: RequestModel = Depends(), db: Session = Depends(get_db)):
    service = UserService(db)
    response = service.get_data(**extract_request_params(request))
    return send_response(status.HTTP_200_OK, "User list successfully", response)


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    response = UserService.get_user(user_id, db)
    return send_response(status.HTTP_200_OK, "User detail successfully", response)


@router.post("/")
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    response = UserService.create_user(user, db)
    return send_response(status.HTTP_201_CREATED, "User create successfully", response)


@router.patch("/{user_id}")
def update_user(user_id: int, user: UpdateUserRequest, db: Session = Depends(get_db)):
    response = UserService.update_user(user_id, user, db)
    return send_response(status.HTTP_200_OK, "User update successfully", response)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    response = UserService.delete_user(user_id, db)
    return send_response(status.HTTP_200_OK, "User deleted successfully", response)
