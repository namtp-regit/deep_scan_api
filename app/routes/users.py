from fastapi import APIRouter

from app.requests.user_request import CreateUserRequest, UpdateUserRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Item 1"}


@router.post("/")
def create_user(user: CreateUserRequest):
    return user


@router.patch("/{user_id}")
def update_user(user_id: int, user: UpdateUserRequest):
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"id": 3}
