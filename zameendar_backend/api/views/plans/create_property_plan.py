from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Plan, PropertyModel, PropertyPlan
from zameendar_backend.api.utils.json_to_python import json_to_python


class CreatePropertyPlan(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        plan_id = request.POST["plan_id"]
        property_id = request.POST["property_id"]
        is_offer_taken = json_to_python(request.POST.get("is_offer_taken", "false"))

        property_model = PropertyModel.objects.get(id=property_id)
        plan = Plan.objects.get(id=plan_id)

        property_plan = PropertyPlan.objects.filter(
            property_model=property_model, is_active=True
        ).first()
        if not property_plan:
            if is_offer_taken:
                plan_expire_on = timezone.now() + relativedelta(
                    days=plan.offer_duration_in_days
                )
            else:
                plan_expire_on = timezone.now() + relativedelta(
                    days=plan.duration_in_days
                )
            property_plan = PropertyPlan.objects.create(
                property_model=property_model,
                plan=plan,
                plan_start_on=timezone.now(),
                plan_expire_on=plan_expire_on,
                is_active=True,
                is_offer_taken=is_offer_taken,
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
