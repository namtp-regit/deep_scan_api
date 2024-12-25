from pydantic import BaseModel, Field
from utils.constants import MAX_STRING, MIN_STRING


class LoginRequest(BaseModel):
    mail_address: str = Field(
        ..., min_length=MIN_STRING, max_length=MAX_STRING, description="Mail address"
    )
    password: str = Field(..., min_length=MIN_STRING, max_length=MAX_STRING, description="Password")
