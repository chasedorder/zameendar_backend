from datetime import datetime

from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.meta_models import PropertyTypes
from zameendar_backend.api.models import Commercial, Property, Seller
from zameendar_backend.api.utils.formatting_date_time import convert_string_to_date
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddCommercial(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        # for updating
        if property_id:
            return update_commerical(request)
        # for adding new
        else:
            return create_commerical(request)


def create_commerical(request):
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")
    commercial_type = request.POST.get("commercial_type")
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")

    commerical_category = request.POST.get("commerical_category")
    price_per_square_feet = request.POST.get("price_per_square_feet")
    builtup_area = request.POST.get("builtup_area")
    price_per_square_yard = request.POST.get("price_per_square_yard")
    passenger_lifts = request.POST.get("passenger_lifts")
    service_lifts = request.POST.get("service_lifts")
    parking_available = json_to_python(request.POST.get("parking_available"))
    min_contract_period = request.POST.get("min_contract_period")
    negotialble = json_to_python(request.POST.get("negotialble"))
    tax_gov_charges_included = json_to_python(request.POST.get("tax_gov_charges_included"))
    dg_ups_charges_included = json_to_python(request.POST.get("dg_ups_charges_included"))
    water_charges_included = json_to_python(request.POST.get("water_charges_included"))
    floor_number = request.POST.get("floor_number")
    possession_date = request.POST.get("possession_date")
    electricity_bill_included = json_to_python(request.POST.get("electricity_bill_included"))
    safety_deposit = request.POST.get("safety_deposit")
    rent_per_month = request.POST.get("rent_per_month")
    current_step = int(request.POST.get("current_step", 0))

    property_map, property_address, seller_contact = add_common_details(
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )
    property = Property.objects.create(
        project_name=project_name,
        seller=seller,
        final_price=final_price,
        property_type=PropertyTypes.Commercial,
        address=property_address,
        seller_contact=seller_contact,
        map=property_map,
        about_property=about_property,
        current_step=current_step,
    )

    Commercial.objects.create(
        property=property,
        commerical_category=commerical_category,
        commercial_type=commercial_type,
        price_per_square_feet=price_per_square_feet,
        builtup_area=builtup_area,
        price_per_square_yard=price_per_square_yard,
        passenger_lifts=passenger_lifts,
        service_lifts=service_lifts,
        parking_available=parking_available,
        min_contract_period=min_contract_period,
        negotialble=negotialble,
        tax_gov_charges_included=tax_gov_charges_included,
        dg_ups_charges_included=dg_ups_charges_included,
        water_charges_included=water_charges_included,
        floor_number=floor_number,
        possession_date=convert_string_to_date(possession_date) if possession_date else None,
        electricity_bill_included=electricity_bill_included,
        safety_deposit=safety_deposit,
        rent_per_month=rent_per_month,
    )

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response(
        {
            "message": "Property Added Successfully",
            "property_id": property.id,
        }
    )


def update_commerical(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")
    commercial_type = request.POST.get("commercial_type")
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")

    commerical_category = request.POST.get("commerical_category")
    price_per_square_feet = request.POST.get("price_per_square_feet")
    builtup_area = request.POST.get("builtup_area")
    price_per_square_yard = request.POST.get("price_per_square_yard")
    passenger_lifts = request.POST.get("passenger_lifts")
    service_lifts = request.POST.get("service_lifts")
    parking_available = json_to_python(request.POST.get("parking_available"))
    min_contract_period = request.POST.get("min_contract_period")
    negotialble = json_to_python(request.POST.get("negotialble"))
    tax_gov_charges_included = json_to_python(request.POST.get("tax_gov_charges_included"))
    dg_ups_charges_included = json_to_python(request.POST.get("dg_ups_charges_included"))
    water_charges_included = json_to_python(request.POST.get("water_charges_included"))
    floor_number = request.POST.get("floor_number")
    possession_date = request.POST.get("possession_date")
    electricity_bill_included = json_to_python(request.POST.get("electricity_bill_included"))
    safety_deposit = request.POST.get("safety_deposit")
    rent_per_month = request.POST.get("rent_per_month")
    current_step = int(request.POST.get("current_step", 0))

    property = Property.objects.get(id=property_id)

    property_map, property_address, seller_contact = add_common_details(
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )
    property.project_name = project_name
    property.seller = seller
    property.final_price = final_price
    property.property_type = PropertyTypes.Commercial
    property.address = property_address
    property.seller_contact = seller_contact
    property.map = property_map
    property.about_property = about_property
    property.updated_date = datetime.now()
    property.current_step = current_step
    property.save()

    commercial = Commercial.objects.get(property=property)
    commercial.commercial_type = commercial_type
    commercial.property = property
    commercial.commerical_category = commerical_category
    commercial.price_per_square_feet = price_per_square_feet
    commercial.builtup_area = builtup_area
    commercial.price_per_square_yard = price_per_square_yard
    commercial.passenger_lifts = passenger_lifts
    commercial.service_lifts = service_lifts
    commercial.parking_available = parking_available
    commercial.min_contract_period = min_contract_period
    commercial.negotialble = negotialble
    commercial.tax_gov_charges_included = tax_gov_charges_included
    commercial.dg_ups_charges_included = dg_ups_charges_included
    commercial.water_charges_included = water_charges_included
    commercial.floor_number = floor_number
    commercial.possession_date = (
        convert_string_to_date(possession_date) if possession_date else None
    )
    commercial.electricity_bill_included = electricity_bill_included
    commercial.safety_deposit = safety_deposit
    commercial.rent_per_month = rent_per_month
    commercial.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response({"property_id": property.id})
