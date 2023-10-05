from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PropertyImage, Seller


class DeletePropertyImage(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        image_id = request.POST.get("image_id")
        propoerty_image = PropertyImage.objects.get(id=image_id)
        seller = Seller.objects.get(user=request.user)

        if propoerty_image.property.seller == seller:
            propoerty_image.delete()
            return send_pass_http_response()
        return send_fail_http_response({"message": "Not Authorized"})
