from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PendingSmsOtp, Seller, User


class SellerSignUp(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"].strip()
        phone_number = request.POST["phone_number"].strip()
        otp = request.POST["otp"].strip()
        is_phone_already_use = User.objects.filter(phone_number=phone_number).exists()
        if is_phone_already_use:
            return send_fail_http_response({"message": "Phone already in use"})
        is_email_already_use = User.objects.filter(email=email).exists()
        if is_email_already_use:
            return send_fail_http_response({"message": "Email already in use"})

        pending_otp = PendingSmsOtp.objects.get(phone=phone_number)
        if int(otp) != pending_otp.otp:
            return send_fail_http_response({"message": "incorrect OTP"})

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save()
        pending_otp.delete()
        Seller.objects.create(user=user)
        token = Token.objects.get(user=user).key
        return send_pass_http_response(
            {
                "message": "User Created Successfully",
                "token": token,
            }
        )
