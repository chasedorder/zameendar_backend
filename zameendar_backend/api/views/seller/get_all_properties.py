from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.models import PropertyModel, Seller
from zameendar_backend.api.serializers.property_serializers import property_serializer


class GetSellerProperties(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        seller = Seller.objects.get(user=request.user)

        properties_queryset = PropertyModel.objects.filter(seller=seller).order_by("-added_date")

        serialzed_data = []
        for property_model in properties_queryset:
            serialzed_data.append(property_serializer(property_model=property_model))

        return JsonResponse({"data": serialzed_data})
