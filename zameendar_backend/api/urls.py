from django.urls import path

from .views.forgot_password import ForgotPassword
from .views.reset_password import ResetPassword
from .views.seller.add_group_appartment import AddGroupAppartment
from .views.seller.seller_signup import SellerSignUp
from .views.send_sms_otp import SendSmsOtp

urlpatterns = [
    path("send_sms_otp/", SendSmsOtp.as_view(), name="send_sms_otp"),
    path("forgot_password/", ForgotPassword.as_view(), name="forgot_password"),
    path("reset_password/", ResetPassword.as_view(), name="reset_password"),
    path("seller_signup/", SellerSignUp.as_view(), name="seller_signup"),
    path("add_group_appartment/", AddGroupAppartment.as_view(), name="add_group_appartment"),
]
