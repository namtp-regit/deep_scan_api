from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.requests.file_request import UploadFileRequest
from app.services.file_service import FileService

# folder upload
UPLOAD_DIR = "public/uploads"
file_service = FileService(upload_dir=UPLOAD_DIR)

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    await UploadFileRequest.validate_file(file)
    saved_path = file_service.save_file(file, subfolder=None, timestamp=True)
    return {"filename": file.filename, "path": saved_path}


@router.get("/{filename}")
async def get_file(filename: str):
    try:
        file_path = file_service.get_file_path(filename, subfolder=None)
        return {"file_path": file_path}
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
