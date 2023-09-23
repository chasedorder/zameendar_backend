from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.models import Property, Seller
from zameendar_backend.api.serializers.property_serializers import property_serializer


class GetSellerProperties(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        seller = Seller.objects.get(user=request.user)

        properties_queryset = Property.objects.filter(seller=seller)

        serialzed_data = []
        for property in properties_queryset:
            serialzed_data.append(property_serializer(property=property))

        return JsonResponse({"data": serialzed_data})
