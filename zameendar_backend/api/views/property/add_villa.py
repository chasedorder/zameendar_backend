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
from zameendar_backend.api.models import Property, Seller, Villa
from zameendar_backend.api.utils.formatting_date_time import convert_string_to_date
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddVilla(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        # for updating
        if property_id:
            return update_villa(request)
        # for adding new
        else:
            return create_villa(request)


def create_villa(request):
    project_name = request.POST.get("project_name")

    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")

    facing = json_to_python(request.POST.get("facing"))
    carpet_area = request.POST.get("carpet_area")
    bedroom_available = json_to_python(request.POST.get("bedroom_available"))  # list of string
    number_of_washrooms = request.POST.get("number_of_washrooms")
    land_size = request.POST.get("land_size")
    land_width = request.POST.get("land_width")
    land_length = request.POST.get("land_length")
    number_of_floors = request.POST.get("number_of_floors")
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    ready_to_occupy = json_to_python(request.POST.get("ready_to_occupy"))
    available_from = convert_string_to_date(request.POST.get("available_from"))
    price_per_square_feet = request.POST.get("price_per_square_feet")
    floors = json_to_python(request.POST.get("floors"))
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    sale_type = request.POST.get("sale_type")
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")
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
        property_type=PropertyTypes.Villa,
        amenities=amenities,
        address=property_address,
        seller_contact=seller_contact,
        map=property_map,
        about_property=about_property,
        current_step=current_step,
    )

    Villa.objects.create(
        property=property,
        facing=facing,
        land_size=land_size,
        land_width=land_width,
        land_length=land_length,
        carpet_area=carpet_area,
        bedroom_available=bedroom_available,
        number_of_washrooms=number_of_washrooms,
        number_of_floors=number_of_floors,
        number_of_car_parking=number_of_car_parking,
        number_of_bike_parking=number_of_bike_parking,
        ready_to_occupy=ready_to_occupy,
        available_from=available_from,
        price_per_square_feet=price_per_square_feet,
        floors=floors,
        furnishing_detail=furnishing_detail,
        sale_type=sale_type,
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


def update_villa(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")
    facing = json_to_python(request.POST.get("facing"))
    carpet_area = request.POST.get("carpet_area")
    bedroom_available = json_to_python(request.POST.get("bedroom_available"))  # list of string
    number_of_washrooms = request.POST.get("number_of_washrooms")
    land_size = request.POST.get("land_size")
    land_width = request.POST.get("land_width")
    land_length = request.POST.get("land_length")
    number_of_floors = request.POST.get("number_of_floors")
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    ready_to_occupy = json_to_python(request.POST.get("ready_to_occupy"))
    available_from = convert_string_to_date(request.POST.get("available_from"))
    price_per_square_feet = request.POST.get("price_per_square_feet")
    floors = json_to_python(request.POST.get("floors"))
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    sale_type = request.POST.get("sale_type")
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")
    current_step = int(request.POST.get("current_step", 0))

    property = Property.objects.get(id=property_id)

    property_map, property_address, seller_contact = update_common_details(
        property=property,
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )

    property.project_name = project_name
    property.seller = seller
    property.final_price = final_price
    property.property_type = PropertyTypes.Villa
    property.amenities = amenities
    property.address = property_address
    property.seller_contact = seller_contact
    property.map = property_map
    property.about_property = about_property
    property.updated_date = datetime.now()
    property.current_step = current_step
    property.save()

    villa = Villa.objects.get(property=property)
    villa.property = property
    villa.facing = facing
    villa.land_size = land_size
    villa.land_width = land_width
    villa.land_length = land_length
    villa.carpet_area = carpet_area
    villa.bedroom_available = bedroom_available
    villa.number_of_washrooms = number_of_washrooms
    villa.number_of_floors = number_of_floors
    villa.number_of_car_parking = number_of_car_parking
    villa.number_of_bike_parking = number_of_bike_parking
    villa.ready_to_occupy = ready_to_occupy
    villa.available_from = available_from
    villa.price_per_square_feet = price_per_square_feet
    villa.floors = floors
    villa.furnishing_detail = furnishing_detail
    villa.sale_type = sale_type
    villa.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response({"property_id": property.id})
