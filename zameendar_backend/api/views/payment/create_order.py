import json

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
from zameendar_backend.api.models import Order, Property, PropertyPlan
from zameendar_backend.api.serializers.order_serializer import OrderSerializer

env = environ.Env()


environ.Env.read_env()


class StartPayment(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.POST["amount"]
        property_id = request.POST["property_id"]

        client = razorpay.Client(auth=(env("RAZORPAY_PUBLIC_KEY"), env("RAZORPAY_SECRET_KEY")))

        property = Property.objects.get(id=property_id)
        property_plan = PropertyPlan.objects.get(property=property)
        final_amount = property_plan.plan.price

        if final_amount == amount:
            payment = client.order.create(
                {"amount": int(final_amount) * 100, "currency": "INR", "payment_capture": "1"}
            )

            order = Order.objects.create(property_plan=property_plan, final_amount=final_amount)

            serializer = OrderSerializer(order)

            data = {"payment": payment, "order": serializer.data}

            return send_pass_http_response(data)


class HandlePaymentSuccess(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        res = json.loads(request.POST["response"])

        order_id = res.get("razorpay_order_id")
        raz_pay_id = res.get("razorpay_payment_id")
        raz_signature = res.get("razorpay_signature")

        order = Order.objects.get(order_payment_id=order_id)

        data = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": raz_pay_id,
            "razorpay_signature": raz_signature,
        }

        client = razorpay.Client(auth=(env("RAZORPAY_PUBLIC_KEY"), env("RAZORPAY_SECRET_KEY")))

        try:
            check = client.utility.verify_payment_signature(data)
        except Exception as e:
            print("Redirect to error url or error page")
            return Response({"error": "Something went wrong"})

        order.isPaid = True
        order.razor_signature = raz_signature
        order.save()
        res_data = {"message": "payment successfully received!"}

        return send_pass_http_response(res_data)
