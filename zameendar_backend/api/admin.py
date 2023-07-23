from django.contrib import admin

from .models import (
    PG,
    Building,
    Flat,
    GroupAppartment,
    GroupPlot,
    GroupVilla,
    OpenPlot,
    PropertyAddress,
    ProperyImage,
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
        "country",
        "linked_property",
    ]

    readonly_fields = ["linked_property"]


admin.site.register(PG)
admin.site.register(UserAddress)
admin.site.register(Building)
admin.site.register(Flat)
admin.site.register(GroupAppartment)
admin.site.register(GroupPlot)
admin.site.register(GroupVilla)
admin.site.register(OpenPlot)
admin.site.register(Rent)
admin.site.register(User)
admin.site.register(Villa)
admin.site.register(ProperyImage)
admin.site.register(PropertyAddress, ProperyAddressAdmin)
