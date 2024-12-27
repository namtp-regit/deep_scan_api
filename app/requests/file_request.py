from pydantic import BaseModel
from fastapi import UploadFile, status
from core.config import settings
from core.send_response import raise_exception


class UploadFileRequest(BaseModel):
    @classmethod
    async def validate_file(cls, file: UploadFile) -> None:
        # Validate type
        if file.content_type not in settings.content_types:
            raise_exception(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f"File type {file.content_type} is not allowed. Allowed types: {settings.content_types}",
            )

        # validate size
        file_size = await file.read()
        if len(file_size) > settings.max_file_size:
            raise_exception(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f"File size exceeds the limit of {settings.max_file_size // (1024 * 1024)} MB.",
            )

        file.file.seek(0)
