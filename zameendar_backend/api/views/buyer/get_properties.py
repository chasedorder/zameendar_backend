from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView

from zameendar_backend.api.meta_models import PropertyTypes
from zameendar_backend.api.models import PropertyPlan
from zameendar_backend.api.serializers.buyer_property_serializers import (
    property_serializers,
)
from zameendar_backend.api.serializers.get_paginated_property_reponse import (
    get_paginated_property_response,
)


class GetProperties(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        page = int(request.GET.get("page", 1))
        property_type = request.GET["property_type"]

        page_size = 10
        offset = (page - 1) * page_size

        property_plans = PropertyPlan.objects.filter(
            Q(order__isPaid=True) | Q(plan__plan_category="Free"),
            is_active=True,
            property_model__property_type__iexact=property_type,
        ).order_by("-plan__weightage")

        properties_queryset = []

        for plan in property_plans:
            if not plan.is_expired:
                properties_queryset.append(plan.property_model)

        serialized_data = []
        for property_model in properties_queryset[offset : offset + page_size]:
            serialized_data.append(property_serializers(property_model=property_model))

        response_data = get_paginated_property_response(
            page, len(serialized_data), serialized_data
        )

        return JsonResponse(response_data)
