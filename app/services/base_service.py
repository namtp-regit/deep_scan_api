from abc import ABC, abstractmethod
import json
from math import ceil
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from sqlalchemy.sql.expression import or_


class BaseService(ABC):
    def __init__(self, model, session: Session):
        self.model = model
        self.session = session
        self.order_dir_map = {"asc": asc, "asc": desc}
        self.search_ables = []
        self.order_ables = {}
        self.filter_ables = {}
        self.per_page = 10

    @abstractmethod
    def make_new_query(self):
        pass

    def apply_search(self, query, search: str):
        if not search or not self.search_ables:
            return query

        content = f"%{search}%"
        search_conditions = [
            getattr(self.model, field).like(content) for field in self.search_ables
        ]
        return query.filter(or_(*search_conditions))

    def apply_filters(self, query, filters: list):
        if not filters:
            return query

        decoded_filters = [json.loads(item) for item in filters]
        for filter_item in decoded_filters:
            key = filter_item.get("key")
            data = filter_item.get("data")
            if key in self.filter_ables and data not in (None, "", "all"):
                filter_func = self.filter_ables.get(key)
                if callable(filter_func):
                    query = filter_func(query, data)
                else:
                    query = query.filter(getattr(self.model, filter_func) == data)
        return query

    def apply_order(self, query, orders: list):
        if not orders:
            return query

        decoded_orders = [json.loads(item) for item in orders]
        for order_item in decoded_orders:
            key = order_item.get("key")
            direction = order_item.get("dir", "asc").lower()
            if key in self.order_ables and direction in self.order_dir_map:
                field = self.order_ables.get(key)
                if "," in field:
                    fields = field.split(",")
                    for f in fields:
                        query = query.order_by(
                            self.order_dir_map[direction](getattr(self.model, f))
                        )
                else:
                    query = query.order_by(
                        self.order_dir_map[direction](getattr(self.model, field))
                    )
        return query

    def paginate(self, query, page: int = 1, per_page: int = None):
        per_page = per_page or self.per_page
        offset = (page - 1) * per_page
        return query.offset(offset).limit(per_page)

    def get_data(self, search=None, filters=None, orders=None, page=1, per_page=None, all=False):
        # query = self.session.query(self.model)

        # apply conditions
        query = self.make_new_query()
        query = self.apply_search(query, search)
        query = self.apply_filters(query, filters)
        query = self.apply_order(query, orders)

        total = query.count()
        per_page = per_page or self.per_page
        total_page = ceil(total / per_page)

        if all:
            return {
                "data": query.all(),
                "total": total,
                "total_page": total_page,
            }

        paginated_query = self.paginate(query, page, per_page)
        return {
            "data": paginated_query.all(),
            "per_page": per_page,
            "current_page": page,
            "total_page": total_page,
            "total": total,
        }
