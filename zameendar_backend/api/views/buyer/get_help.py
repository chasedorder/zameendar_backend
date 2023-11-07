from django.http import JsonResponse
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Help


class GetHelp(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        name = request.GET.get("name")
        email = request.GET.get("email")
        message = request.GET.get("message")
        phone = request.GET.get("phone")

        Help.objects.create(name=name, email=email, phone_number=phone, message=message)

        return send_pass_http_response()
