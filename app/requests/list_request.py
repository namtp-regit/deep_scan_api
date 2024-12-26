from pydantic import BaseModel, Field
from typing import List, Optional, Tuple


class RequestModel(BaseModel):
    search: Optional[str] = Field(None, description="Search")
    filters: Optional[List[str]] = Field(None, description="Filters in JSON format")
    orders: Optional[List[str]] = Field(None, description="Orders in JSON format")
    page: int = Field(1, description="Page number", ge=1)
    per_page: int = Field(10, description="Number of items per page", ge=1)
    all: Optional[bool] = Field(False, description="Return all records without pagination if True")
