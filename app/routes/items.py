from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
def get_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

@router.post("/")
def create_item(name: str):
    return {"id": 3, "name": name}