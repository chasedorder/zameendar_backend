from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.meta_models import PropertyTypes
from zameendar_backend.api.models import Property
from zameendar_backend.api.serializers.buyer_property_serializers import property_serializers
from zameendar_backend.api.serializers.get_paginated_property_reponse import (
    get_paginated_property_response,
)


class GetAllGroupVilla(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        page = int(request.GET.get("page", 1))
        page_size = 10
        offset = (page - 1) * page_size
        property_type = PropertyTypes.GroupVilla
        properties_queryset = Property.objects.filter(property_type=property_type)[
            offset : offset + page_size
        ]
        serialized_data = []
        for property in properties_queryset:
            serialized_data.append(property_serializers(property=property))

        response_data = get_paginated_property_response(page, property_type, serialized_data)

        return JsonResponse(response_data)
