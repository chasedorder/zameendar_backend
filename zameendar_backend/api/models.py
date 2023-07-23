from django import forms
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_better_admin_arrayfield.models.fields import ArrayField
from mptt.models import MPTTModel, TreeForeignKey

from .meta_models import PROPERTY_CATEGORY


class ChoiceArrayField(ArrayField):
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
        return super(ArrayField, self).formfield(**defaults)


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


class PendingUser(models.Model):
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20)


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PropertyAddress(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code},\
              {self.country}"

    def linked_property(self):
        # Check if there's a linked property (GroupAppartment or GroupVilla)
        if hasattr(self, "groupappartment"):
            # return getattr(self, "groupappartment").name
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        "admin:api_groupappartment_change",
                        args=[getattr(self, "groupappartment").pk],
                    ),
                    getattr(self, "groupappartment").name,
                )
            )
        elif hasattr(self, "groupvilla"):
            return getattr(self, "groupvilla").name
        return "N/A"


class Property(models.Model):
    GroupAppart = "Group Appartment"
    GroupVilla = "Group Villa"
    GroupPlot = "Group Plot"
    Flat = "Flat"
    Building = "Building"
    Villa = "Villa"
    OpenPlot = "Open Plot"
    PG = "PG"
    Rent = "Rent"
    name = models.CharField(max_length=100)
    property_type = models.CharField(
        max_length=50,
        choices=(
            (GroupAppart, "GroupAppartment"),
            (GroupVilla, "GroupVilla"),
            (GroupPlot, "GroupPlot"),
            (Flat, "Flat"),
            (Building, "Building"),
            (Villa, "Villa"),
            (OpenPlot, "OpenPlot"),
            (PG, "PG"),
            (Rent, "Rent"),
        ),
    )
    address = models.OneToOneField(
        PropertyAddress,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    end_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    ready_to_occupy = models.BooleanField(default=False)
    amenities = ArrayField(models.JSONField(), null=True, blank=True, default=list)
    number_of_carparking = models.IntegerField()
    number_of_bike_parking = models.IntegerField()w 


class PropertyHistory(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    property_added_date = models.DateTimeField(auto_now_add=True)
    meta_data = ArrayField(models.JSONField(), null=True, blank=True, default=list)

    def __str__(self) -> str:
        return self.property.name


class ProperyImage(models.Model):
    image = models.ImageField(upload_to="property_images/")
    title = models.CharField(max_length=100, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    meta_data = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return self.title


class GatedPropertyMixin(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    current_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100, null=True)

    read_to_move_in = models.BooleanField(default=False)

    bhk_pricings = ArrayField(models.JSONField(), null=True, blank=True, default=list)

    possession_date = models.DateTimeField(null=True, blank=True)

    address = models.OneToOneField(
        PropertyAddress,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class SinglePropertyMixin(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    current_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    read_to_move_in = models.BooleanField(default=False)

    address = models.OneToOneField(
        PropertyAddress,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class GroupAppartment(GatedPropertyMixin, models.Model):
    pass


class GroupVilla(GatedPropertyMixin, models.Model):
    pass


class GroupPlot(GatedPropertyMixin, models.Model):
    pass


class Flat(SinglePropertyMixin, models.Model):
    pass


class Building(SinglePropertyMixin, models.Model):
    pass


class Villa(SinglePropertyMixin, models.Model):
    pass


class OpenPlot(SinglePropertyMixin, models.Model):
    pass


class Rent(SinglePropertyMixin, models.Model):
    pass


class PG(SinglePropertyMixin, models.Model):
    pass


class PropertyMap(models.Model):
    location = models.CharField(max_length=100, null=True)
    property_type = models.CharField(choices=PROPERTY_CATEGORY)
    property = models.OneToOneField(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.property.name


class Plan(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class PropertyPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    current_plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    plan_start_on = models.DateField(null=True, blank=True)
    plan_expire_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        active_plans = PropertyPlan.objects.filter(is_active=True)
        if self.is_active and active_plans.exists():
            raise ValidationError(
                "An active plan already exists. Cannot save another active plan."
            )
        self.is_active = True
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.property.name


class Order(models.Model):
    property = models.ForeignKey(Property, on_delete=models.DO_NOTHING)
    final_amount = models.DecimalField(max_digits=8, decimal_places=2)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    order_id = models.CharField(
        unique=True, max_length=100, null=True, blank=True, default=None
    )
    date_of_payment = models.DateTimeField(default=timezone.now)
    # razorpay
    razorpay_order_id = models.CharField(max_length=100000, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100000, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100000, null=True, blank=True)
    is_payment_successful = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.date_of_payment and self.pk:
            self.order_id = self.date_of_payment.strftime("PAY2ME%Y%m%dODR") + str(
                self.pk
            )

        return super().save(*args, **kwargs)


class SellerPayment(models.Model):
    seller = models.ForeignKey("Seller", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=1000)
    amount = models.DecimalField(
        decimal_places=2, max_digits=100, null=True, blank=True
    )


@receiver(post_delete, sender=GroupAppartment)
@receiver(post_delete, sender=GroupVilla)
def delete_address_on_property_delete(sender, instance, **kwargs):
    if instance.address:
        instance.address.delete()
