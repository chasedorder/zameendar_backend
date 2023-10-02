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


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class ContactDetails(models.Model):
    phone_number_1 = models.CharField(max_length=50, blank=True, null=True)
    phone_number_2 = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True)


class PropertyAddress(models.Model):
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
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
    about_property = models.TextField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

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
    number_of_floors = models.IntegerField(null=True, blank=True)
    ready_to_occupy = models.BooleanField(default=False, null=True, blank=True)
    possession_date = models.DateField(null=True, blank=True)
    number_of_car_parking = models.IntegerField(null=True, blank=True)
    number_of_bike_parking = models.IntegerField(null=True, blank=True)
    project_area = models.CharField(max_length=1000, null=True, blank=True)
    project_size = models.CharField(max_length=1000, null=True, blank=True)
    rera_id = models.CharField(max_length=1000, null=True, blank=True)
    sale_type = models.CharField(max_length=1000, null=True, blank=True)
    property_age = models.CharField(max_length=100, null=True, blank=True)
    number_of_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_bathrooms = models.PositiveIntegerField(null=True, blank=True)
    facing = ChoiceArrayField(
        models.CharField(max_length=50, choices=FACINGS.facing_choices),
        default=list,
        null=True,
        blank=True,
    )
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=100, choices=FursnihingTypes.furnished_choices),
        default=list,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.property.project_name


class GroupVilla(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    # Pricing Details
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    bhk_details = ArrayField(models.JSONField(), default=list, null=True, blank=True)
    # Property Details
    number_of_floors = ArrayField(
        models.CharField(max_length=100), null=True, blank=True, default=list
    )
    land_area_sizes = ArrayField(
        models.CharField(max_length=100), null=True, blank=True, default=list
    )
    ready_to_occupy = models.BooleanField(default=False, null=True, blank=True)
    possession_date = models.DateField(null=True, blank=True)

    number_of_car_parking = models.IntegerField(null=True, blank=True)
    number_of_bike_parking = models.IntegerField(null=True, blank=True)
    land_width = models.CharField(max_length=50, blank=True)
    land_length = models.CharField(max_length=50, blank=True)
    total_project_area = models.CharField(max_length=100, null=True, blank=True)
    rera_id = models.CharField(max_length=100, null=True, blank=True)
    facing = ChoiceArrayField(
        models.CharField(max_length=50, choices=FACINGS.facing_choices),
        default=list,
        null=True,
        blank=True,
    )
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=100, choices=FursnihingTypes.furnished_choices),
        default=list,
        null=True,
        blank=True,
    )
    project_size = models.CharField(max_length=50, null=True, blank=True)
    sale_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.property.project_name


class GroupPlot(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    price_per_sqyd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    plot_sizes = ArrayField(models.CharField(max_length=50), default=list, null=True, blank=True)
    total_project_area = models.CharField(max_length=100, null=True, blank=True)
    rera_id = models.CharField(max_length=100, null=True, blank=True)
    facing = ChoiceArrayField(
        models.CharField(max_length=50, choices=FACINGS.facing_choices),
        default=list,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.property.project_name


# Single Poroperties
class Flat(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = ChoiceArrayField(
        models.CharField(max_length=50, choices=FACINGS.facing_choices),
        default=list,
        null=True,
        blank=True,
    )
    carpet_area = models.CharField(max_length=100, null=True, blank=True)
    bedroom_available = ArrayField(
        models.CharField(max_length=50), default=list, null=True, blank=True
    )
    number_of_washrooms = models.IntegerField(null=True, blank=True)
    floor_number = models.IntegerField(null=True, blank=True)
    number_of_car_parking = models.IntegerField(null=True, blank=True)
    number_of_bike_parking = models.IntegerField(null=True, blank=True)
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=100, choices=FursnihingTypes.furnished_choices),
        default=list,
        null=True,
        blank=True,
    )
    ready_to_occupy = models.BooleanField(default=False, null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    price_per_square_feet = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sale_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.property.project_name


class Building(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = ChoiceArrayField(
        models.CharField(max_length=50, choices=FACINGS.facing_choices),
        default=list,
        null=True,
        blank=True,
    )
    land_size = models.CharField(max_length=50, null=True, blank=True)
    land_width = models.CharField(max_length=50, null=True, blank=True)
    land_length = models.CharField(max_length=50, null=True, blank=True)
    carpet_area = models.CharField(max_length=100, null=True, blank=True)
    number_of_floors = models.IntegerField(null=True, blank=True)
    number_of_car_parking = models.IntegerField(null=True, blank=True)
    number_of_bike_parking = models.IntegerField(null=True, blank=True)
    ready_to_occupy = models.BooleanField(default=False, null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    sale_type = models.CharField(max_length=100, null=True, blank=True)
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=100, choices=FursnihingTypes.furnished_choices),
        default=list,
        null=True,
        blank=True,
    )
    bedroom_available = ArrayField(
        models.CharField(max_length=50), default=list, null=True, blank=True
    )

    def __str__(self):
        return self.property.project_name


class Villa(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = ChoiceArrayField(
        models.CharField(max_length=50, choices=FACINGS.facing_choices),
        null=True,
        blank=True,
        default=list,
    )
    land_size = models.CharField(max_length=50, null=True, blank=True)
    land_width = models.CharField(max_length=50, null=True, blank=True)
    land_length = models.CharField(max_length=50, null=True, blank=True)
    carpet_area = models.CharField(max_length=100, null=True, blank=True)
    bedroom_available = ArrayField(
        models.CharField(max_length=50), null=True, blank=True, default=list
    )
    number_of_washrooms = models.IntegerField(null=True, blank=True)
    number_of_floors = models.CharField(max_length=50, null=True, blank=True)
    number_of_car_parking = models.IntegerField(null=True, blank=True)
    number_of_bike_parking = models.IntegerField(null=True, blank=True)
    ready_to_occupy = models.BooleanField(default=False, null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    price_per_square_feet = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    floors = ArrayField(models.CharField(max_length=100), null=True, blank=True, default=list)
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=100, choices=FursnihingTypes.furnished_choices),
        null=True,
        blank=True,
        default=list,
    )
    sale_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.property.project_name


class OpenPlot(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    facing = ChoiceArrayField(
        models.CharField(max_length=50, choices=FACINGS.facing_choices),
        null=True,
        blank=True,
        default=list,
    )
    land_size = models.CharField(max_length=50, null=True, blank=True)
    land_width = models.CharField(max_length=50, null=True, blank=True)
    land_length = models.CharField(max_length=50, null=True, blank=True)
    is_fencing = models.BooleanField(default=False, null=True, blank=True)
    price_per_square_yard = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.property.project_name


# PG And Rents
class Rent(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    rent_type = models.CharField(max_length=100, null=True, blank=True)
    facing = ChoiceArrayField(
        models.CharField(max_length=50, choices=FACINGS.facing_choices),
        default=list,
        null=True,
        blank=True,
    )
    floor_number = models.IntegerField(null=True, blank=True)
    number_of_car_parking = models.IntegerField(null=True, blank=True)
    number_of_bike_parking = models.IntegerField(null=True, blank=True)
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=100, choices=FursnihingTypes.furnished_choices),
        null=True,
        blank=True,
        default=list,
    )
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ready_to_move_in = models.BooleanField(default=False, null=True, blank=True)
    carpet_area = models.CharField(max_length=100, null=True, blank=True)
    bedroom_available = ArrayField(
        models.CharField(max_length=50), default=list, null=True, blank=True
    )

    def __str__(self):
        return self.property.project_name


class PG(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    sharing_type = ArrayField(models.CharField(max_length=50), null=True, blank=True, default=list)
    sharing_for = ArrayField(models.CharField(max_length=50), null=True, blank=True, default=list)
    attached_washroom = models.BooleanField(default=False, null=True, blank=True)
    food_facility = models.BooleanField(default=False, null=True, blank=True)
    parking_facility = models.BooleanField(default=False, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_facilities = ArrayField(
        models.JSONField(),
        default=list,
        null=True,
        blank=True,
    )
    ready_to_move_in = models.BooleanField(default=False, null=True, blank=True)
    coliving_common_area = models.CharField(max_length=100, null=True, blank=True)
    non_veg_available = models.BooleanField(default=False, null=True, blank=True)
    visitor_allowed = models.BooleanField(default=False, null=True, blank=True)
    opposite_sex_visitor_allowed = models.BooleanField(default=False, null=True, blank=True)
    drinking_allowed = models.BooleanField(default=False, null=True, blank=True)
    smoking_allowed = models.BooleanField(default=False, null=True, blank=True)
    any_time_allowed = models.BooleanField(default=False, null=True, blank=True)
    last_time_entry = models.CharField(null=True, blank=True)
    furnishing_detail = ChoiceArrayField(
        models.CharField(max_length=100, choices=FursnihingTypes.furnished_choices),
        null=True,
        blank=True,
        default=list,
    )
    food_offerings = ArrayField(
        models.CharField(max_length=100),
        null=True,
        blank=True,
        default=list,
    )

    def __str__(self):
        return self.property.project_name


class Commercial(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    commercial_type = models.CharField(max_length=100, null=True, blank=True)
    commerical_category = models.CharField(max_length=100, null=True, blank=True)
    price_per_square_feet = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    builtup_area = models.CharField(max_length=100, null=True, blank=True)
    price_per_square_yard = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    passenger_lifts = models.IntegerField(null=True, blank=True)
    service_lifts = models.IntegerField(null=True, blank=True)
    parking_available = models.BooleanField(default=False, null=True, blank=True)
    min_contract_period = models.CharField(max_length=100, null=True, blank=True)
    negotialble = models.BooleanField(default=False, null=True, blank=True)
    tax_gov_charges_included = models.BooleanField(default=False, null=True, blank=True)
    dg_ups_charges_included = models.BooleanField(default=False, null=True, blank=True)
    water_charges_included = models.BooleanField(default=False, null=True, blank=True)
    floor_number = models.IntegerField(null=True, blank=True)
    possesstion_date = models.DateTimeField(null=True, blank=True)
    electricity_bill_included = models.BooleanField(default=False, null=True, blank=True)
    safety_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.property.project_name


class Plan(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_in_months = models.IntegerField(null=True, blank=True)
    description = ArrayField(models.JSONField(), null=True, blank=True, default=list)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class PropertyPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    plan_start_on = models.DateField(null=True, blank=True)
    plan_expire_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        active_plans = PropertyPlan.objects.filter(is_active=True, property=self.property)
        if self.is_active and active_plans.exists():
            raise ValidationError(
                "An plan for this property already exists. Cannot save another plan."
            )
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
    PropertyTypes.Commercial: Commercial,
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
