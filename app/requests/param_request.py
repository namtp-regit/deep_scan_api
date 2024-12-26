from fastapi import Query
from typing import List, Optional


class RequestModel:
    def __init__(
        self,
        search: Optional[str] = Query(None, description="Search"),
        filters: Optional[List[str]] = Query(None, description="Filters in JSON format"),
        orders: Optional[List[str]] = Query(None, description="Orders in JSON format"),
        page: int = Query(1, description="Page number", ge=1),
        per_page: int = Query(10, description="Number of items per page", ge=1),
        all: Optional[bool] = Query(
            False, description="Return all records without pagination if True"
        ),
    ):
        self.search = search
        self.filters = filters
        self.orders = orders
        self.page = page
        self.per_page = per_page
        self.all = all
