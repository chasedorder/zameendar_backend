from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Buyer, PropertyModel, WishList


class RemoveFromWishlist(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST["property_id"]
        buyer = Buyer.objects.get(user=request.user)

        property_model = PropertyModel.objects.get(id=property_id)
        wishlist = WishList.objects.filter(buyer=buyer).first()

        if not wishlist:
            wishlist = WishList.objects.create(buyer=buyer)
        wishlist.properties.remove(property_model)

        return send_pass_http_response({"message": "removed from wishlist"})
