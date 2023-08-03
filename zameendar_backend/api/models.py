import os

from django import forms
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields import ArrayField as arrayfield
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_better_admin_arrayfield.models.fields import ArrayField
from rest_framework.authtoken.models import Token

from .meta_models import *


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class ChoiceArrayField(arrayfield):

    """
    A field that allows us to store an array of choices.

    Uses Django 1.9's postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(arrayfield, self).formfield(**defaults)


class UserAddress(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    address_line_2 = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code},\
              {self.country}"


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    last_active = models.DateTimeField(auto_now=True, blank=True)
    email = models.EmailField(unique=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username


class PendingSmsOtp(models.Model):
    phone = models.CharField(max_length=20)
    otp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.phone


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class ContactDetails(models.Model):
    phone_number_1 = models.CharField(max_length=50, blank=True)
    phone_number_2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)


class PropertyAddress(models.Model):
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    area = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.street_address}, {self.area}, {self.city}, {self.state},\
              {self.postal_code},"

    def linked_property(self):
        if hasattr(self, "property"):
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        "admin:api_property_change",
                        args=[getattr(self, "property").pk],
                    ),
                    getattr(self, "property").project_name,
                )
            )
        return "N/A"


class PropertyMap(models.Model):
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.location

    def linked_property(self):
        if hasattr(self, "property"):
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        "admin:api_property_change",
                        args=[getattr(self, "property").pk],
                    ),
                    getattr(self, "property").project_name,
                )
            )
        return "N/A"


class Property(models.Model):
    project_name = models.CharField(max_length=100)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=50, choices=PropertyTypes.property_type_choices)
    address = models.OneToOneField(
        PropertyAddress,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    map = models.OneToOneField(
        PropertyMap,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    seller_contact = models.OneToOneField(
        ContactDetails, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    start_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    end_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amenities = ArrayField(models.JSONField(), default=list)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.project_name


class PropertyImage(models.Model):
    image = models.ImageField(upload_to="property_images/")
    title = models.CharField(max_length=100, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    meta_data = models.JSONField(default=dict)

    def __str__(self):
        return self.title


# Group Properties
class GroupAppartment(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    # Pricing Details
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    bhk_details = ArrayField(models.JSONField(), default=list)
    # Property Details
    number_of_floors = models.IntegerField()
    ready_to_occupy = models.BooleanField(default=False)
    possession_date = models.DateField(null=True, blank=True)
    number_of_car_parking = models.IntegerField()
    number_of_bike_parking = models.IntegerField()

    def __str__(self):
        return self.property.project_name


class GroupVilla(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    # Pricing Details
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    bhk_details = ArrayField(models.JSONField(), default=list)
    # Property Details
    number_of_floors = ArrayField(
        models.CharField(max_length=100), null=True, blank=True, default=list
    )
    land_area_sizes = ArrayField(
        models.CharField(max_length=100), null=True, blank=True, default=list
    )
    ready_to_occupy = models.BooleanField(default=False)
    possession_date = models.DateField(null=True, blank=True)

    number_of_car_parking = models.IntegerField()
    number_of_bike_parking = models.IntegerField()
    land_width = models.CharField(max_length=50, blank=True)
    land_length = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.property.project_name


class GroupPlot(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    price_per_sqyd = models.DecimalField(max_digits=10, decimal_places=2)
    plot_sizes = ArrayField(models.CharField(max_length=50), default=list)

    def __str__(self):
        return self.property.project_name


# Single Poroperties
class Flat(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = models.CharField(max_length=10, choices=FACINGS.facing_choices)
    carpet_area = models.CharField(max_length=100)
    bedroom_available = ArrayField(models.CharField(max_length=50), default=list)
    number_of_washrooms = models.IntegerField()
    floor_number = models.IntegerField()
    number_of_car_parking = models.IntegerField()
    number_of_bike_parking = models.IntegerField()
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=100, choices=FursnihingTypes.furnished_choices),
        null=True,
        blank=True,
        default=list,
    )
    ready_to_occupy = models.BooleanField(default=False)
    available_from = models.DateField()

    def __str__(self):
        return self.property.project_name


class Building(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = models.CharField(max_length=10, choices=())
    land_size = models.CharField(max_length=50)
    land_width = models.CharField(max_length=50)
    land_length = models.CharField(max_length=50)
    carpet_area = models.CharField(max_length=100)
    number_of_floors = models.IntegerField()
    number_of_car_parking = models.IntegerField()
    number_of_bike_parking = models.IntegerField()
    ready_to_occupy = models.BooleanField(default=False)
    available_from = models.DateField()

    def __str__(self):
        return self.property.project_name


class Villa(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = models.CharField(max_length=10, choices=FACINGS.facing_choices)
    land_size = models.CharField(max_length=50)
    land_width = models.CharField(max_length=50)
    land_length = models.CharField(max_length=50)
    carpet_area = models.CharField(max_length=100)
    bedroom_available = ArrayField(models.CharField(max_length=50), default=list)
    number_of_washrooms = models.IntegerField()
    number_of_floors = models.CharField(max_length=50)
    number_of_car_parking = models.IntegerField()
    number_of_bike_parking = models.IntegerField()
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=1000, choices=FursnihingTypes.furnished_choices), default=list
    )
    ready_to_occupy = models.BooleanField(default=False)
    available_from = models.DateField()

    def __str__(self):
        return self.property.project_name


class OpenPlot(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = models.CharField(max_length=10, choices=FACINGS.facing_choices)
    land_size = models.CharField(max_length=50)
    land_width = models.CharField(max_length=50)
    land_length = models.CharField(max_length=50)
    is_fencing = models.BooleanField(default=False)

    def __str__(self):
        return self.property.project_name


# PG And Rents
class Rent(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = ArrayField(models.CharField(max_length=50), default=list)
    floor_number = models.IntegerField(null=True, blank=True)
    number_of_car_parking = models.IntegerField()
    number_of_bike_parking = models.IntegerField()
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=1000, choices=FursnihingTypes.furnished_choices), default=list
    )
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    ready_to_move_in = models.BooleanField(default=False)

    def __str__(self):
        return self.property.project_name


class PG(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    sharing_type = ArrayField(models.CharField(max_length=50), default=list)
    sharing_for = ArrayField(models.CharField(max_length=50), default=list)
    attached_washroom = models.BooleanField(default=False)
    food_facility = models.BooleanField(default=False)
    parking_facility = models.BooleanField(default=False)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    other_facilities = ArrayField(models.JSONField(), default=list)
    ready_to_move_in = models.BooleanField(default=False)

    def __str__(self):
        return self.property.project_name


class Plan(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_in_months = models.FloatField(null=True, blank=True)
    description = ArrayField(models.JSONField(), null=True, blank=True, default=list)

    def __str__(self):
        return self.title


class PropertyPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    plan = models.OneToOneField(Plan, on_delete=models.DO_NOTHING)
    plan_start_on = models.DateField(null=True, blank=True)
    plan_expire_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        active_plans = PropertyPlan.objects.filter(is_active=True)
        if self.is_active and active_plans.exists():
            raise ValidationError("An active plan already exists. Cannot save another active plan.")
        self.is_active = True
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.property.project_name


class Order(models.Model):
    property_plan = models.ForeignKey(PropertyPlan, on_delete=models.DO_NOTHING)
    final_amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    date_of_payment = models.DateTimeField(default=timezone.now)
    # razorpay
    razorpay_order_id = models.CharField(max_length=100000, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100000, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100000, null=True, blank=True)
    is_payment_successful = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.date_of_payment and self.pk:
            self.order_id = self.date_of_payment.strftime("PAY2ME%Y%m%dODR") + str(self.pk)

        return super().save(*args, **kwargs)


class SellerPayment(models.Model):
    seller = models.ForeignKey("Seller", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=1000)
    amount = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)


PROPERTY_MODEL_MAP = {
    PropertyTypes.GroupAppart: GroupAppartment,
    PropertyTypes.GroupVilla: GroupVilla,
    PropertyTypes.GroupPlot: GroupPlot,
    PropertyTypes.Flat: Flat,
    PropertyTypes.Villa: Villa,
    PropertyTypes.Building: Building,
    PropertyTypes.OpenPlot: OpenPlot,
    PropertyTypes.Rent: Rent,
    PropertyTypes.PG: PG,
}


# <<<<<<<<<<<<<<<<<< SIGNALS >>>>>>>>>>>>>>>>>>>>


@receiver(post_delete, sender=Property)
def delete_address_on_property_delete(sender, instance: Property, **kwargs):
    model_class = PROPERTY_MODEL_MAP.get(instance.property_type)
    if model_class:
        model_class.objects.filter(property=instance).delete()

    PropertyImage.objects.filter(property=instance).delete()

    if instance.address:
        instance.address.delete()
    if instance.seller_contact:
        instance.seller_contact.delete()
    if instance.map:
        instance.map.delete()
