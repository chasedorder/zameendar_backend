from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.models import Buyer, PropertyModel, WishList


class IsInWishlist(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        property_id = request.POST["property_id"]
        property_obj = PropertyModel.objects.get(id=property_id)
        buyer = Buyer.objects.get(user=request.user)

        in_wishlist = False
        if WishList.objects.filter(buyer=buyer, properties=property_obj):
            in_wishlist = True

        return JsonResponse({"message": in_wishlist})
