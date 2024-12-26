from typing import Optional
from pydantic import BaseModel, field_validator


class CreateUserRequest(BaseModel):
    name: str
    email: str

    # Validator tùy chỉnh
    @field_validator("name")
    def name_cannot_contain_special_chars(cls, v):
        if not v.isalnum():
            raise ValueError("name must be alphanumeric")
        return v


class UpdateUserRequest(CreateUserRequest):
    email: Optional[int] = None
