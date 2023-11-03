from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Buyer, PendingSmsOtp, Seller, User
from zameendar_backend.api.serializers.token_serializer import UserSerializer


def get_user_type(user):
    serializer_data = UserSerializer(user).data
    first_name = serializer_data.get("first_name")
    last_name = serializer_data.get("last_name")
    phone_number = serializer_data.get("phone_number")
    username = serializer_data.get("username")

    is_seller = Seller.objects.filter(user=user).exists()
    is_buyer = Buyer.objects.filter(user=user).exists()

    return {
        "first_name": first_name,
        "last_name": last_name,
        "is_seller": is_seller,
        "is_buyer": is_buyer,
        "phone_number": phone_number,
        "username": username,
    }


class BuyerSignUp(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
        password = request.POST["password"].strip()
        phone_number = request.POST["phone_number"].strip()
        otp = request.POST["otp"].strip()

        if Buyer.objects.filter(user__phone_number=phone_number).exists():
            return send_fail_http_response({"message": "Phone already in use"})

        pending_otp = PendingSmsOtp.objects.get(phone=phone_number)
        if int(otp) != pending_otp.otp:
            return send_fail_http_response({"message": "incorrect OTP"})

        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            try:
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=phone_number,
                    phone_number=phone_number,
                )
                user.set_password(password)
                user.save()
            except Exception as e:
                return send_fail_http_response({"message": str(e)})

        Buyer.objects.create(user=user)
        token = Token.objects.get(user=user).key
        pending_otp.delete()

        return send_pass_http_response(
            {
                "message": "User Created Successfully",
                "token": token,
                "user_type": get_user_type(user=user),
            }
        )
