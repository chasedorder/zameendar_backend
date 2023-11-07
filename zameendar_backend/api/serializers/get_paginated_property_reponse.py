from django.conf import settings

from zameendar_backend.api.meta_models import PropertyTypes
from zameendar_backend.api.models import PropertyModel


def get_paginated_property_response(page, total_items, data):
    page_size = settings.PAGE_SIZE
    total_pages = (total_items + page_size - 1) // page_size  # Calculate total pages

    response_data = {
        "data": data,
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
    }

    # Calculate next and previous page numbers
    if page < total_pages:
        response_data["next_page"] = page + 1
    if page > 1:
        response_data["previous_page"] = page - 1

    return response_data
