from datetime import date

from dateutil.relativedelta import relativedelta
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

        property_plan = PropertyPlan.objects.filter(property=property, is_active=True).first()
        if not property_plan:
            property_plan = PropertyPlan.objects.create(
                property=property,
                plan=plan,
                plan_start_on=date.today(),
                plan_expire_on=date.today() + relativedelta(months=plan.duration_in_months),
                is_active=True,
            )

            return send_pass_http_response(
                {
                    "message": "property plan created successfully",
                    "property_plan_id": property_plan.id,
                }
            )
        else:
            return send_pass_http_response(
                {
                    "message": "property plan already exist",
                    "plan_id": property_plan.plan.id,
                    "property_plan_id": property_plan.id,
                }
            )
