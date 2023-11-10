from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView

from zameendar_backend.api.models import PropertyPlan
from zameendar_backend.api.serializers.buyer_property_serializers import (
    property_serializers,
)
from zameendar_backend.api.serializers.get_paginated_property_reponse import (
    get_paginated_property_response,
)


class GetSearchProperties(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        property_plans = PropertyPlan.objects.filter(
            Q(order__isPaid=True) | Q(plan__plan_category="Free"),
            is_active=True,
        ).order_by("-plan__weightage")

        properties_queryset = []

        for plan in property_plans:
            if not plan.is_expired:
                properties_queryset.append(plan.property_model)

        serialized_data = []
        for property_model in properties_queryset:
            serialized_data.append(
                {
                    "property_id": property_model.id,
                    "project_name": property_model.project_name,
                    "project_type": property_model.property_type,
                    "location": property_model.map.location
                    if property_model.map
                    else "",
                }
            )

        return JsonResponse({"data": serialized_data})
