from datetime import date

from dateutil.relativedelta import relativedelta
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Plan, Property, PropertyPlan
from zameendar_backend.api.utils.json_to_python import json_to_python


class UpgradePropertyPlan(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        plan_id = request.POST["plan_id"]
        property_id = request.POST["property_id"]
        is_offer_taken = json_to_python(request.POST.get("is_offer_taken", "false"))

        property = Property.objects.get(id=property_id)
        plan = Plan.objects.get(id=plan_id)

        # deactivating old plan
        old_property_plan = PropertyPlan.objects.filter(property=property, is_active=True).first()
        old_property_plan.is_active = False
        old_property_plan.save()

        # upgrading to new plan
        if is_offer_taken:
            plan_expire_on = date.today() + relativedelta(months=plan.offer_duration_in_months)
        else:
            plan_expire_on = date.today() + relativedelta(months=plan.duration_in_months)
        property_plan = PropertyPlan.objects.create(
            property=property,
            plan=plan,
            plan_start_on=date.today(),
            plan_expire_on=plan_expire_on,
            is_active=True,
            is_offer_taken=is_offer_taken,
        )

        return send_pass_http_response(
            {
                "message": "property plan upgraded successfully",
                "property_plan_id": property_plan.id,
            }
        )
