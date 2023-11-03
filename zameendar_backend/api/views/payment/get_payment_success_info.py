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
from zameendar_backend.api.models import Order

env = environ.Env()


environ.Env.read_env()


class GetPaymentSuccessInfo(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        res = json.loads(request.POST["response"])

        order_id = res.get("razorpay_order_id")
        raz_pay_id = res.get("razorpay_payment_id")
        raz_signature = res.get("razorpay_signature")

        order = Order.objects.get(razorpay_order_id=order_id)

        data = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": raz_pay_id,
            "razorpay_signature": raz_signature,
        }

        client = razorpay.Client(auth=(env("RAZORPAY_PUBLIC_KEY"), env("RAZORPAY_SECRET_KEY")))

        try:
            check = client.utility.verify_payment_signature(data)
        except Exception as e:
            print("Redirect to error url or error page", e)
            return send_fail_http_response({"error": "Something went wrong"})

        order.isPaid = True
        order.razorpay_signature = raz_signature
        order.razorpay_payment_id = raz_pay_id
        order.save()
        res_data = {"message": "payment successfully received!"}

        return send_pass_http_response(res_data)
