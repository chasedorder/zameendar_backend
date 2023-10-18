from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Adjust this value as needed
    page_size_query_param = (
        "page_size"  # You can optionally allow clients to specify page size via a query parameter
    )
