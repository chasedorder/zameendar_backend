from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import (
    PG,
    Building,
    ContactDetails,
    Flat,
    GroupAppartment,
    GroupPlot,
    GroupVilla,
    OpenPlot,
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
)


class PropertyAdmin(admin.ModelAdmin):
    list_display = ["project_name"]


class ProperyAddressAdmin(admin.ModelAdmin):
    list_display = [
        "street_address",
        "city",
        "state",
        "postal_code",
        "linked_property",
    ]

    readonly_fields = ["linked_property"]


class PropertyMapAdmin(admin.ModelAdmin):
    list_display = ["location", "linked_property"]

    readonly_fields = ["linked_property"]


class PropertyImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(
            '<img src="{}" style="object-fit: cover; width: 200px; height: 200px;" />'.format(
                obj.image.url
            )
        )

    image_tag.short_description = "Image"

    fields = ["image_tag"]
    readonly_fields = ["image_tag"]


class UserAdmin(BaseUserAdmin):
    # add_fieldsets = (
    #     (
    #         None,
    #         {
    #             "fields": (
    #                 "email",
    #                 "username",
    #                 "password1",
    #                 "password2",
    #                 "phone_number",
    #                 "last_active",
    #             )
    #         },
    #     ),
    #     ("Permissions", {"fields": ("is_superuser", "is_staff")}),
    # )
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


admin.site.register(Seller)
admin.site.register(Plan)
admin.site.register(PropertyMap, PropertyMapAdmin)
admin.site.register(PropertyPlan)
admin.site.register(Property, PropertyAdmin)
admin.site.register(ContactDetails)
admin.site.register(PG)
admin.site.register(UserAddress)
admin.site.register(Building)
admin.site.register(Flat)
admin.site.register(GroupAppartment)
admin.site.register(GroupPlot)
admin.site.register(GroupVilla)
admin.site.register(OpenPlot)
admin.site.register(Rent)
admin.site.register(User, UserAdmin)
admin.site.register(Villa)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(PendingSmsOtp)
admin.site.register(PropertyAddress, ProperyAddressAdmin)
