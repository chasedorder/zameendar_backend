from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PropertyModel


class DeleteSellerProperty(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        property_id = request.POST["property_id"]

        PropertyModel.objects.get(id=property_id).delete()

        return send_pass_http_response()
