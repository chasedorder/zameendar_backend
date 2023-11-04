from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.meta_models import PropertyTypes
from zameendar_backend.api.models import Buyer, Property
from zameendar_backend.api.serializers.buyer_property_serializers import property_serializers
from zameendar_backend.api.serializers.get_paginated_property_reponse import (
    get_paginated_property_response,
)


class GetPropertyDetails(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        property_id = request.GET.get("property_id")

        property = Property.objects.get(id=property_id)
        serialized_data = property_serializers(property=property)

        return JsonResponse(serialized_data)
