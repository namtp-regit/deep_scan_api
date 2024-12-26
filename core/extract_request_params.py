from app.requests.list_request import RequestModel


def extract_request_params(request: RequestModel):
    return {
        "search": request.search,
        "filters": request.filters,
        "orders": request.orders,
        "page": request.page,
        "per_page": request.per_page,
        "all": request.all,
    }
