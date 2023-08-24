from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PendingSmsOtp, User


class ResetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        password = request.POST["password"]
        otp = request.POST["otp"]

        if email:
            user = User.objects.get(email=email)
            phone_number = user.phone_number

        pending_otp = PendingSmsOtp.objects.get(phone=phone_number)

        if int(otp) != pending_otp.otp:
            return send_fail_http_response({"message": "incorrect OTP"})

        user = User.objects.get(phone_number=phone_number)
        user.set_password(password)
        user.save()
        pending_otp.delete()
        return send_pass_http_response({"message": "Password Reset Successfully"})
