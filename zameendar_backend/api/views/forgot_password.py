import json

from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PendingSmsOtp, User

from ..utils.generate_otp import generate_six_digit_otp, sendSMS


class ForgotPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        phone = request.GET.get("phone")
        email = request.GET.get("email")

        if phone:
            user = User.objects.filter(phone_number=phone).first()
            if not user:
                return send_fail_http_response({"message": "phone number not registered"})
        else:
            user = User.objects.filter(email=email).first()
            if not user:
                return send_fail_http_response({"message": "email not registered"})
        phone = user.phone_number
        otp = generate_six_digit_otp()
        pending_otp, _ = PendingSmsOtp.objects.get_or_create(phone=phone)
        pending_otp.otp = int(otp)
        pending_otp.save()
        resp = sendSMS("apikey", phone, "Zameendar Properties", otp)
        resp = json.loads(resp.decode("utf-8"))
        if resp["status"] == "failure":
            return send_fail_http_response(
                {"message": "Some error occur", "otp only for testing": otp}
            )
        return send_pass_http_response(
            {"message": "OTP sent successfully", "phone_number": user.phone_number}
        )
