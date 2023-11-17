import environ
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.mail.send_email_otp import send_email_otp
from zameendar_backend.api.models import PendingEmailOtp
from zameendar_backend.api.utils.generate_otp import generate_six_digit_otp

env = environ.Env()


environ.Env.read_env()


class SendSignupEmailOtp(APIView):
    authentication_classes = []

    permission_classes = []

    def get(self, request):
        email = request.GET["email"]

        otp = generate_six_digit_otp()

        pending_otp, _ = PendingEmailOtp.objects.get_or_create(email=email)

        pending_otp.otp = int(otp)

        pending_otp.save()

        try:
            send_email_otp(email=email, otp=otp)
            return send_pass_http_response(
                {
                    "message": "OTP sent successfully",
                    "otp only for testing": otp,
                }
            )
        except Exception as e:
            return send_fail_http_response(
                {
                    "message": f"Some error occur {e}",
                    "otp only for testing": otp,
                }
            )
