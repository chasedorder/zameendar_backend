from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PendingEmailOtp, User


class ResetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        otp = request.POST["otp"]

        user = User.objects.get(email=email)

        pending_otp = PendingEmailOtp.objects.get(email=email)

        if int(otp) != pending_otp.otp:
            return send_fail_http_response({"message": "incorrect OTP"})

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        pending_otp.delete()
        return send_pass_http_response(
            {
                "message": "Password Reset Successfully",
            }
        )
