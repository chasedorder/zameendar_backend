from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import PropertyImage, Seller
from zameendar_backend.api.utils.json_to_python import json_to_python


class UpdatePropertyImage(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        image_id = request.POST.get("image_id")
        image = request.FILES.get("image")
        title = request.POST.get("title")
        meta_data = json_to_python(request.POST.get("meta_data"))
        propoerty_image = PropertyImage.objects.get(id=image_id)
        seller = Seller.objects.get(user=request.user)

        if propoerty_image.property_model.seller == seller:
            if image:
                propoerty_image.image = image
            if title:
                propoerty_image.title = title
            if meta_data:
                propoerty_image.meta_data = meta_data

            propoerty_image.save()

            return send_pass_http_response()
        return send_fail_http_response({"message": "Not Authorized"})
