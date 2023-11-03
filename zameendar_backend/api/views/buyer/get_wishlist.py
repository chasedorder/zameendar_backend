from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import Buyer, WishList


class GetWishlist(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        buyer = Buyer.objects.get(user=request.user)
        wishlist_obj = WishList.objects.filter(buyer=buyer).first()
        serialized_wishlist = []
        if wishlist_obj:
            for property in wishlist_obj.properties.all():
                serialized_wishlist.append(
                    {
                        "id": property.id,
                        "project_name": property.project_name,
                        "property_type": property.property_type,
                        "start_price": property.start_price,
                        "end_price": property.end_price,
                        "final_price": property.final_price,
                        "location": property.map.location if property.map else "",
                    }
                )

        return JsonResponse({"wishlist": serialized_wishlist})
