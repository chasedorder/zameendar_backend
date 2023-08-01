from django.urls import path

from .views.forgot_password import ForgotPassword
from .views.payment.create_order import CreateOrder
from .views.payment.create_property_plan import CreatePropertyPlan
from .views.payment.get_all_plans import GetAllPlans
from .views.property.add_building import AddBuilding
from .views.property.add_flat import AddFlat
from .views.property.add_group_appartment import AddGroupAppartment
from .views.property.add_group_plot import AddGroupPlot
from .views.property.add_group_villas import AddGroupVilla
from .views.property.add_open_plot import AddOpenPlot
from .views.property.add_pg import AddPG
from .views.property.add_rent import AddRent
from .views.property.add_villa import AddVilla
from .views.reset_password import ResetPassword
from .views.seller.seller_signup import SellerSignUp
from .views.send_signup_sms_otp import SendSignupSmsOtp

urlpatterns = [
    path("send_signup_sms_otp/", SendSignupSmsOtp.as_view(), name="send_signup_sms_otp"),
    path("seller_signup/", SellerSignUp.as_view(), name="seller_signup"),
    path("forgot_password/", ForgotPassword.as_view(), name="forgot_password"),
    path("reset_password/", ResetPassword.as_view(), name="reset_password"),
    path("add_group_appartment/", AddGroupAppartment.as_view(), name="add_group_appartment"),
    path("add_group_villa/", AddGroupVilla.as_view(), name="add_group_villa"),
    path("add_group_plot/", AddGroupPlot.as_view(), name="add_group_plot"),
    path("add_flat/", AddFlat.as_view(), name="add_flat"),
    path("add_building/", AddBuilding.as_view(), name="add_building"),
    path("add_villa/", AddVilla.as_view(), name="add_villa"),
    path("add_open_plot/", AddOpenPlot.as_view(), name="add_open_plot"),
    path("add_rent/", AddRent.as_view(), name="add_rent"),
    path("add_pg/", AddPG.as_view(), name="add_pg"),
    path("get_all_plans/", GetAllPlans.as_view(), name="get_all_plans"),
    path("create_property_plan/", CreatePropertyPlan.as_view(), name="create_property_plan"),
    path("create_order/", CreateOrder.as_view(), name="create_order"),
]
