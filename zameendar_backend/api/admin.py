from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import (
    PG,
    PROPERTY_MODEL_MAP,
    Building,
    Buyer,
    Commercial,
    ContactDetails,
    Flat,
    GroupAppartment,
    GroupPlot,
    GroupVilla,
    OpenPlot,
    Order,
    PendingSmsOtp,
    Plan,
    Property,
    PropertyAddress,
    PropertyImage,
    PropertyMap,
    PropertyPlan,
    Rent,
    Seller,
    User,
    UserAddress,
    Villa,
    WishList,
)


class PlanAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["title", "plan_type", "id"]


class SellerAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


class BuyerAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


class PropertyPlanAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


class ContactDetailsAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


class UserAddressAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


class WishListAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


# base properties to show in each property category in admin panel
class BasePropertyAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["property", "id", "get_property_id", "base_property"]

    @admin.display(description="Property id")
    def get_property_id(self, obj):
        return obj.property.id

    def base_property(self, obj):
        if hasattr(obj, "property"):
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        "admin:api_property_change",
                        args=[getattr(obj, "property").pk],
                    ),
                    "basic_details",
                )
            )
        return "N/A"

    readonly_fields = ["base_property"]


class PropertyAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["project_name", "id", "seller", "added_date", "property_details"]

    def property_details(self, obj):
        if hasattr(obj, "property_type"):
            property_category_obj = PROPERTY_MODEL_MAP[obj.property_type].objects.get(property=obj)
            category_model_class_name = property_category_obj._meta.model_name.lower()
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        f"admin:api_{category_model_class_name}_change",
                        args=[property_category_obj.pk],
                    ),
                    obj.project_name,
                )
            )
        return "N/A"

    readonly_fields = ["property_details"]


class PendingSmsOtpAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


class ProperyAddressAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = [
        "street_address",
        "city",
        "state",
        "postal_code",
        "base_property",
    ]

    def base_property(self, obj):
        if hasattr(obj, "property"):
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        "admin:api_property_change",
                        args=[getattr(obj, "property").pk],
                    ),
                    getattr(obj, "property").project_name,
                )
            )
        return "N/A"

    readonly_fields = ["base_property"]


class PropertyMapAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["location", "base_property"]

    def base_property(self, obj):
        if hasattr(obj, "property"):
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        "admin:api_property_change",
                        args=[getattr(obj, "property").pk],
                    ),
                    getattr(obj, "property").project_name,
                )
            )
        return "N/A"

    readonly_fields = ["base_property"]


class PropertyImageAdmin(admin.ModelAdmin, DynamicArrayMixin):
    def image_tag(self, obj):
        return format_html(
            '<img src="{}" style="object-fit: cover; width: 200px; height: 200px;" />'.format(
                obj.image.url
            )
        )

    image_tag.short_description = "Image"

    fields = ["image_tag", "image", "title", "property", "meta_data"]
    readonly_fields = ["image_tag"]


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "phone_number",
                )
            },
        ),
        ("Permissions", {"fields": ("is_superuser", "is_staff")}),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password",
                    "phone_number",
                )
            },
        ),
        ("Permissions", {"fields": ("is_superuser", "is_staff")}),
    )
    list_display = ["username", "email", "last_active"]
    # search_fields = ("email", "username")


class OrderAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ["razorpay_order_id", "order_date", "id"]


admin.site.register(User, UserAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(PendingSmsOtp, PendingSmsOtpAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(PropertyPlan, PropertyPlanAdmin)
admin.site.register(ContactDetails, ContactDetailsAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(PropertyMap, PropertyMapAdmin)
admin.site.register(PropertyAddress, ProperyAddressAdmin)

# properties
admin.site.register(Property, PropertyAdmin)
admin.site.register(GroupAppartment, BasePropertyAdmin)
admin.site.register(GroupVilla, BasePropertyAdmin)
admin.site.register(GroupPlot, BasePropertyAdmin)
admin.site.register(Flat, BasePropertyAdmin)
admin.site.register(Building, BasePropertyAdmin)
admin.site.register(Villa, BasePropertyAdmin)
admin.site.register(OpenPlot, BasePropertyAdmin)
admin.site.register(PG, BasePropertyAdmin)
admin.site.register(Rent, BasePropertyAdmin)
admin.site.register(Commercial, BasePropertyAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Order, OrderAdmin)
