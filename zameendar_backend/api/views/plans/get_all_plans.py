from django.http import JsonResponse
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.models import Plan


class GetAllPlans(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        plans = Plan.objects.filter(is_active=True)

        plans_details = []

        for plan in plans:
            plans_details.append(
                {
                    "id": plan.id,
                    "title": plan.title,
                    "base_price": plan.base_price,
                    "offer_price": plan.offer_price,
                    "description": plan.description,
                    "duration_in_months": plan.duration_in_months,
                    "offer_duration_in_months": plan.offer_duration_in_months,
                    "plan_type": plan.plan_type,
                }
            )
        return JsonResponse({"plans_details": plans_details})
