from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

@router.get("/{user_id}")
def get_item(user_id: int):
    return {"id": 1, "name": "Item 1"}

@router.post("/")
def create_item(name: str):
    return {"id": 3, "name": name}

@router.patch("/{user_id}")
def update_item(user_id: int, name: str):
    return {"id": 3, "name": name}

@router.delete("/{user_id}")
def delete_item(user_id: int):
    return {"id": 3}
