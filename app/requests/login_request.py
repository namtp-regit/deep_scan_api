from typing import Optional
from pydantic import BaseModel, Field
from utils.constants import MAX_STRING, MIN_STRING


class LoginRequest(BaseModel):
    mail_address: str = Field(
        ..., min_length=MIN_STRING, max_length=MAX_STRING, description="Mail address"
    )
    password: str = Field(..., min_length=MIN_STRING, max_length=MAX_STRING, description="Password")


class AdminSchema(BaseModel):
    id: int
    name: str
    mail_address: str
    created_at: str
    updated_at: str
    role: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    me: Optional[AdminSchema]
