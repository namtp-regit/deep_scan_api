from fastapi import APIRouter, Depends, status
from app.requests.param_request import RequestModel
from app.requests.user_request import CreateUserRequest, UpdateUserRequest
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from core.extract_request_params import extract_request_params
from core.send_response import send_response
from database.connect import get_db

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("/")
def get_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_users()


@router.get("/list")
def list(request: RequestModel = Depends(), user_service: UserService = Depends(get_user_service)):
    response = user_service.get_data(**extract_request_params(request))
    return send_response(status.HTTP_200_OK, "User list successfully", response)


@router.get("/{user_id}")
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    response = user_service.get_user(user_id)
    return send_response(status.HTTP_200_OK, "User detail successfully", response)


@router.post("/")
def create_user(user: CreateUserRequest, user_service: UserService = Depends(get_user_service)):
    response = user_service.create_user(user)
    return send_response(status.HTTP_201_CREATED, "User create successfully", response)


@router.patch("/{user_id}")
def update_user(
    user_id: int, user: UpdateUserRequest, user_service: UserService = Depends(get_user_service)
):
    response = user_service.update_user(user_id, user)
    return send_response(status.HTTP_200_OK, "User update successfully", response)


@router.delete("/{user_id}")
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    response = user_service.delete_user(user_id)
    return send_response(status.HTTP_200_OK, "User deleted successfully", response)
