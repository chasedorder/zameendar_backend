from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from zameendar_backend.api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = (
        #     "id",
        #     "email",
        #     "username",
        #     "password",
        # )
        fields = "__all__"


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
    class Meta:
        model = Token
        fields = ("key", "user")
