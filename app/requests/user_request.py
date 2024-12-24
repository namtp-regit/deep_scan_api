from typing import Optional
from pydantic import BaseModel, field_validator


class CreateUserRequest(BaseModel):
    username: str
    email: str
    age: int

    # Validator tùy chỉnh
    @field_validator("username")
    def username_cannot_contain_special_chars(cls, v):
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v


class UpdateUserRequest(CreateUserRequest):
    age: Optional[int] = None
