from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.mail.send_email_otp import send_email_otp
from zameendar_backend.api.models import PendingEmailOtp, User

from ..utils.generate_otp import generate_six_digit_otp


class ForgotPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # phone = request.GET.get("phone")
        email = request.GET.get("email")

        user = User.objects.filter(email=email).first()
        if not user:
            return send_fail_http_response({"message": "email not registered"})
        otp = generate_six_digit_otp()
        pending_otp, _ = PendingEmailOtp.objects.get_or_create(email=email)
        pending_otp.otp = int(otp)
        pending_otp.save()
        try:
            send_email_otp(email=email, otp=otp)
            return send_pass_http_response(
                {"message": "OTP sent successfully", "email": email}
            )

        except Exception as e:
            return send_fail_http_response(
                {
                    "message": f"Some error occur {e}",
                    "otp only for testing": otp,
                }
            )
