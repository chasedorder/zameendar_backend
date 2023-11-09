from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.meta_models import PropertyTypes
from zameendar_backend.api.models import Buyer, PropertyImage, Rent, WishList


class GetWishlist(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        buyer = Buyer.objects.filter(user=request.user).first()
        if not buyer:
            return send_pass_http_response({"wishlist": []})
        wishlist_obj = WishList.objects.filter(buyer=buyer).first()
        serialized_wishlist = []
        if wishlist_obj:
            for property_model in wishlist_obj.properties.all():
                image_obj = PropertyImage.objects.filter(
                    property_model=property_model
                ).first()
                image = image_obj.image.url if image_obj else None
                rent_per_month = None
                if property_model.property_type == PropertyTypes.Rent:
                    try:
                        rent_per_month = Rent.objects.get(
                            property_model=property_model
                        ).rent_per_month
                    except Rent.DoesNotExist:
                        rent_per_month = None

                serialized_wishlist.append(
                    {
                        "id": property_model.id,
                        "project_name": property_model.project_name,
                        "property_type": property_model.property_type,
                        "start_price": property_model.start_price,
                        "end_price": property_model.end_price,
                        "final_price": property_model.final_price,
                        "rent_per_month": rent_per_month,
                        "image": image,
                        "location": property_model.map.location
                        if property_model.map
                        else "",
                    }
                )

        return JsonResponse({"wishlist": serialized_wishlist})
