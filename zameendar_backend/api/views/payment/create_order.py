import environ
import razorpay
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Order, PropertyPlan
from zameendar_backend.api.serializers.order_serializer import OrderSerializer

env = environ.Env()


environ.Env.read_env()


class CreateOrder(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        property_plan_id = request.POST["property_plan_id"]

        client = razorpay.Client(auth=(env("RAZORPAY_PUBLIC_KEY"), env("RAZORPAY_SECRET_KEY")))

        property_plan = PropertyPlan.objects.get(id=property_plan_id)

        if not property_plan.is_active:
            return send_fail_http_response({"message": "property plan is not active"})

        if property_plan.is_offer_taken:
            final_amount = property_plan.plan.offer_price
        else:
            final_amount = property_plan.plan.base_price

        if final_amount:
            payment = client.order.create(
                {
                    "amount": int(final_amount) * 100,
                    "currency": "INR",
                    "payment_capture": "0",
                    "receipt": "receipt#1",
                    "notes": {},
                }
            )

            order = Order.objects.create(
                property_plan=property_plan,
                final_amount=final_amount,
                razorpay_order_id=payment["id"],
            )

            serializer = OrderSerializer(order)

            data = {"payment": payment, "order": serializer.data}

            return send_pass_http_response(data)
        return send_fail_http_response({"message": "base price or offer price is empty"})
