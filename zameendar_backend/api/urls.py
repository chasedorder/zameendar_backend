import random

from django.urls import path

from .views.buyer.add_to_wishlist import AddToWishlist
from .views.buyer.buyer_signup import BuyerSignUp
from .views.buyer.get_all_building import GetAllBuilding
from .views.buyer.get_all_commercial import GetAllCommercial
from .views.buyer.get_all_flat import GetAllFlat
from .views.buyer.get_all_group_appartment import GetAllGroupAppartments
from .views.buyer.get_all_group_plot import GetAllGroupPlot
from .views.buyer.get_all_group_villa import GetAllGroupVilla
from .views.buyer.get_all_open_plot import GetAllOpenPlot
from .views.buyer.get_all_pg import GetAllPg
from .views.buyer.get_all_rent import GetAllRent
from .views.buyer.get_all_villa import GetAllVilla
from .views.buyer.get_wishlist import GetWishlist

# seller
from .views.forgot_password import ForgotPassword
from .views.payment.create_order import CreateOrder
from .views.payment.get_payment_success_info import GetPaymentSuccessInfo
from .views.plans.create_property_plan import CreatePropertyPlan
from .views.plans.delete_property_plan import DeletePropertyPlan
from .views.plans.get_all_plans import GetAllPlans
from .views.plans.get_property_plan_details import GetPropertyPlanDetail
from .views.property.add_building import AddBuilding
from .views.property.add_commercial import AddCommercial
from .views.property.add_flat import AddFlat
from .views.property.add_group_appartment import AddGroupAppartment
from .views.property.add_group_plot import AddGroupPlot
from .views.property.add_group_villas import AddGroupVilla
from .views.property.add_open_plot import AddOpenPlot
from .views.property.add_pg import AddPG
from .views.property.add_rent import AddRent
from .views.property.add_villa import AddVilla
from .views.property.delete_property_image import DeletePropertyImage
from .views.property.update_property_image import UpdatePropertyImage
from .views.reset_password import ResetPassword
from .views.seller.get_all_properties import GetSellerProperties
from .views.seller.get_property_details import GetSellerPropertyDetails
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
    path("add_commercial/", AddCommercial.as_view(), name="add_commercial"),
    path("get_all_plans/", GetAllPlans.as_view(), name="get_all_plans"),
    path("create_property_plan/", CreatePropertyPlan.as_view(), name="create_property_plan"),
    path("create_order/", CreateOrder.as_view(), name="create_order"),
    path(
        "get_payment_success_info/",
        GetPaymentSuccessInfo.as_view(),
        name="get_payment_success_info",
    ),
    path("get_seller_properties/", GetSellerProperties.as_view(), name="get_seller_properties"),
    path("delete_property_image/", DeletePropertyImage.as_view(), name="delete_property_image"),
    path("update_property_image/", UpdatePropertyImage.as_view(), name="update_property_image"),
    path(
        "get_property_plan_details/",
        GetPropertyPlanDetail.as_view(),
        name="get_property_plan_details",
    ),
    path(
        "get_seller_property_details/",
        GetSellerPropertyDetails.as_view(),
        name="get_seller_property_details",
    ),
    path("delete_property_plan/", DeletePropertyPlan.as_view(), name="delete_property_plan"),
    # buyer
    path("buyer_signup/", BuyerSignUp.as_view(), name="buyer_signup"),
    path(
        "get_all_group_appartments/",
        GetAllGroupAppartments.as_view(),
        name="get_all_group_appartments",
    ),
    path("get_all_group_villa/", GetAllGroupVilla.as_view(), name="get_all_group_villa"),
    path("get_all_group_plot/", GetAllGroupPlot.as_view(), name="get_all_group_plot"),
    path("get_all_flat/", GetAllFlat.as_view(), name="get_all_flat"),
    path("get_all_building/", GetAllBuilding.as_view(), name="get_all_building"),
    path("get_all_villa/", GetAllVilla.as_view(), name="get_all_villa"),
    path("get_all_open_plot/", GetAllOpenPlot.as_view(), name="get_all_open_plot"),
    path("get_all_rent/", GetAllRent.as_view(), name="get_all_rent"),
    path("get_all_pg/", GetAllPg.as_view(), name="get_all_pg"),
    path("get_all_commercial/", GetAllCommercial.as_view(), name="get_all_commercial"),
    path("add_to_wishlist/", AddToWishlist.as_view(), name="add_to_wishlist"),
    path("get_wishlist/", GetWishlist.as_view(), name="get_wishlist"),
]
