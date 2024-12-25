from fastapi import APIRouter, Depends
from app.requests.user_request import CreateUserRequest, UpdateUserRequest
from app.services import user_service
from sqlalchemy.orm import Session
from database.connect import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Item 1"}


@router.post("/")
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)


@router.patch("/{user_id}")
def update_user(user_id: int, user: UpdateUserRequest, db: Session = Depends(get_db)):
    return user_service.update_user(user_id, user, db)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(user_id, db)
