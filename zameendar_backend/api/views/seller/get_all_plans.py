from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.models import Plan


class GetAllPlans(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        plans = Plan.objects.all()

        plans_details = []

        for plan in plans:
            plans_details.append(
                {
                    "id": plan.id,
                    "title": plan.title,
                    "price": plan.price,
                    "description": plan.description,
                }
            )
        return JsonResponse({"plans_details": plans_details})
