from datetime import date

from dateutil.relativedelta import relativedelta
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Order, PropertyPlan


class DeletePropertyPlan(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        property_plan_id = request.POST["property_plan_id"]

        property_plan = PropertyPlan.objects.get(id=property_plan_id)

        paid_property_plan_order_queryset = Order.objects.filter(
            property_plan=property_plan, isPaid=True
        )
        if paid_property_plan_order_queryset:
            return send_fail_http_response({"message": "Order for this property plan already paid"})
        property_plan.delete()
        return send_pass_http_response(
            {
                "message": "property plan with id {} deleted successfully".format(property_plan_id),
            }
        )
