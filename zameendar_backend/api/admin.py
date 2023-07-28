from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    PG,
    Building,
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
    User,
    UserAddress,
    Villa,
)


class ProperyAddressAdmin(admin.ModelAdmin):
    list_display = [
        "street_address",
        "city",
        "state",
        "postal_code",
        "linked_property",
    ]

    readonly_fields = ["linked_property"]


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


admin.site.register(Plan)
admin.site.register(PropertyMap)
admin.site.register(PropertyPlan)
admin.site.register(Property)
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
admin.site.register(PropertyImage)
admin.site.register(PendingSmsOtp)
admin.site.register(PropertyAddress, ProperyAddressAdmin)
