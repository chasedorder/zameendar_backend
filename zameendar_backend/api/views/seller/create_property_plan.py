from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Plan, Property, PropertyPlan


class CreatePropertyPlan(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        plan_id = request.POST["plan_id"]
        property_id = request.POST["property_id"]

        property = Property.objects.get(id=property_id)
        plan = Plan.objects.get(id=plan_id)

        property_plan, is_new = PropertyPlan.objects.get_or_create(property=property)

        property_plan.plan = plan
        property_plan.save()

        return send_pass_http_response(
            {
                "message": "property plan created successfully",
                "property_plan_id": property_plan.id,
            }
        )
