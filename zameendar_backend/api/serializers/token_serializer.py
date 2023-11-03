from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from zameendar_backend.api.models import Buyer, Seller, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "username",
        )


class CustomRegisterSerializer(RegisterSerializer):
    is_consumer = serializers.BooleanField()
    designation = serializers.CharField()

    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "designation", "user_type", "is_consumer")

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "email": self.validated_data.get("email", ""),
            "designation": self.validated_data.get("designation", ""),
            "is_consumer": self.validated_data.get("is_consumer", ""),
            "user_type": self.validated_data.get("user_type", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_consumer = self.cleaned_data.get("is_consumer")
        user.user_type = self.cleaned_data.get("user_type")
        user.designation = self.cleaned_data.get("designation")
        user.username = self.cleaned_data.get("email")
        user.email = self.cleaned_data.get("email")
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ("key", "user", "user_type")

    def get_user_type(self, obj):
        serializer_data = UserSerializer(obj.user).data
        first_name = serializer_data.get("first_name")
        last_name = serializer_data.get("last_name")
        email = serializer_data.get("email")
        phone_number = serializer_data.get("phone_number")

        is_seller = Seller.objects.filter(user=obj.user).exists()
        is_buyer = Buyer.objects.filter(user=obj.user).exists()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_seller": is_seller,
            "is_buyer": is_buyer,
            "phone_number": phone_number,
        }
