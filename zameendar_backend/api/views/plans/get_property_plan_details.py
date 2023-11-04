from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.models import PropertyModel, PropertyPlan


class GetPropertyPlanDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        property_id = request.GET["property_id"]

        property_model = PropertyModel.objects.get(id=property_id)

        property_plan = PropertyPlan.objects.filter(
            property_model=property_model, is_active=True
        ).first()

        if property_plan:
            serialized_data = {
                "property_plan_id": property_plan.id,
                "plan_id": property_plan.plan.id,
                "plan_start_on": property_plan.plan_start_on,
                "plan_expire_on": property_plan.plan_expire_on,
            }

            return JsonResponse(
                {
                    "data": serialized_data,
                }
            )
        else:
            return send_fail_http_response({"message": "No Plan Created for this Property"})
