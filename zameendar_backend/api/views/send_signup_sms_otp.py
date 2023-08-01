import json

import environ
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PendingSmsOtp
from zameendar_backend.api.utils.generate_otp import generate_six_digit_otp, sendSMS

env = environ.Env()


environ.Env.read_env()


class SendSignupSmsOtp(APIView):
    authentication_classes = []

    permission_classes = []

    def get(self, request):
        phone = request.GET["phone"]

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

        return send_pass_http_response({"message": "OTP sent successfully"})
