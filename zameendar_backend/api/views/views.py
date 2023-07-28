import json

import environ
import razorpay
from django.shortcuts import HttpResponse, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..dispatchers.responses.send_fail_http_response import send_fail_http_response
from ..dispatchers.responses.send_pass_http_response import send_pass_http_response
from ..models import Order, PendingSmsOtp, User
from ..utils.generate_otp import generate_six_digit_otp, sendSMS

env = environ.Env()


environ.Env.read_env()


# @method_decorator(csrf_exempt, name="dispatch")
# class StartPayment(APIView):
#     def post(self, request):
#         amount = request.POST["amount"]
#         name = request.POST["name"]

#         client = razorpay.Client(
#             auth=(env("RAZORPAY_PUBLIC_KEY"), env("RAZORPAY_SECRET_KEY"))
#         )

#         payment = client.order.create(
#             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         )

#         order = Order.objects.create(
#             order_product=name, order_amount=amount, order_payment_id=payment["id"]
#         )

#         serializer = OrderSerializer(order)

#         data = {"payment": payment, "order": serializer.data}

#         return Response(data)


# @method_decorator(csrf_exempt, name="dispatch")
# class HandlePaymentSuccess(APIView):
#     def post(self, request):
#         res = json.loads(request.POST["response"])

#         order_id = res.get("razorpay_order_id", "order_MFVLvLQrKbJQpR")
#         raz_pay_id = res.get("razorpay_payment_id", "pay_MFVMAFLjzdOprY")
#         raz_signature = res.get("razorpay_signature", "pl_MFVLY8Z1fgDbQv")

#         order = Order.objects.get(order_payment_id=order_id)

#         data = {
#             "razorpay_order_id": order_id,
#             "razorpay_payment_id": raz_pay_id,
#             "razorpay_signature": raz_signature,
#         }

#         client = razorpay.Client(
#             auth=(env("RAZORPAY_PUBLIC_KEY"), env("RAZORPAY_SECRET_KEY"))
#         )

#         try:
#             check = client.utility.verify_payment_signature(data)
#         except Exception as e:
#             print("Redirect to error url or error page")
#             return Response({"error": "Something went wrong"})

#         order.isPaid = True
#         order.razor_signature = raz_signature
#         order.save()
#         res_data = {"message": "payment successfully received!"}

#         return Response(res_data)


@csrf_exempt
def send_sms_otp(request):
    phone = request.GET["phone"]
    otp = generate_six_digit_otp()
    pending_otp, is_new = PendingSmsOtp.objects.get_or_create(phone=phone)
    pending_otp.otp = int(otp)
    pending_otp.save()
    resp = sendSMS("apikey", phone, "Zameendar Properties", otp)
    resp = json.loads(resp.decode("utf-8"))
    if resp["status"] == "failure":
        return send_fail_http_response({"message": "Some error occur"})
    return send_pass_http_response({"message": "OTP sent successfully"})
