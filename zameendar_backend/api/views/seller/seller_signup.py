from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PendingSmsOtp, Seller, User


@method_decorator(csrf_exempt, name="dispatch")
class SellerSignUp(APIView):
    def post(self, request):
        name = request.POST["name"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"].strip()
        phone_number = request.POST["phone_number"].strip()
        otp = request.GET["otp"].strip()
        is_phone_already_use = User.objects.filter(phone_number=phone_number).exists()
        if is_phone_already_use:
            return send_fail_http_response("Phone already in use")
        is_email_already_use = User.objects.filter(email=email).exists()
        if is_email_already_use:
            return send_fail_http_response("Email already in use")

        pending_otp = PendingSmsOtp.objects.get(phone=phone_number)
        if int(otp) != pending_otp.otp:
            return send_fail_http_response("incorrect OTP")

        user = User.objects.create(
            username=name, email=email, phone_number=phone_number
        )
        user.set_password(password)
        Seller.objects.create(user=user)

        return send_pass_http_response("User Created Successfully")
