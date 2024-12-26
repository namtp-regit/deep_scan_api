from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from app.requests.user_request import CreateUserRequest, UpdateUserRequest
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from core.send_response import send_response
from database.connect import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return UserService.get_users(db)


@router.get("/list")
def list(
    search: str = Query(None, description="Search"),
    filters: Optional[List[str]] = Query(None, description="Filters in JSON format"),
    orders: Optional[List[str]] = Query(None, description="Orders in JSON format"),
    page: int = Query(1, description="Page number"),
    per_page: int = Query(10, description="Number of items per page"),
    db: Session = Depends(get_db),
):
    service = UserService(db)
    response = service.get_data(
        search=search, filters=filters, orders=orders, page=page, per_page=per_page
    )
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
