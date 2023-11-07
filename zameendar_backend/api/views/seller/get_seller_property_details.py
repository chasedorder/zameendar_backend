from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.models import PropertyModel, Seller
from zameendar_backend.api.serializers.property_serializers import property_serializer


class GetSellerPropertyDetails(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        seller = Seller.objects.get(user=request.user)
        property_id = request.GET["property_id"]
        property_model = PropertyModel.objects.get(id=property_id)
        if not seller == property_model.seller:
            return send_fail_http_response({"message": "Not Authorized"})

        serialzed_data = property_serializer(property_model=property_model)

        return JsonResponse({"data": serialzed_data})