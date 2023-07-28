from django.urls import path

from .views.seller.add_group_appartment import AddGroupAppartment
from .views.views import send_sms_otp

urlpatterns = [
    path("send_sms_otp", send_sms_otp),
    path("add_group_appartment", AddGroupAppartment.as_view(), name="add_group_appartment"),
]
