from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.models import PropertyModel, PropertyPlan
from zameendar_backend.api.serializers.buyer_property_serializers import (
    property_serializers,
)


class GetPropertyDetails(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        property_id = request.GET.get("property_id")

        property_model = PropertyModel.objects.get(id=property_id)

        property_plans = PropertyPlan.objects.filter(
            Q(order__isPaid=True) | Q(plan__plan_category="Free"),
            property_model=property_model,
            is_active=True,
        )
        property_model.views += 1
        property_model.save()

        if property_plans:
            if property_plans.first().is_expired:
                return send_fail_http_response(
                    {"message": "you can't view this property details"}
                )
            return JsonResponse(
                {"data": property_serializers(property_model=property_model)}
            )
        return send_fail_http_response(
            {"message": "you can't view this property details"}
        )
