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
from zameendar_backend.api.models import Building, Property, Seller
from zameendar_backend.api.utils.formatting_date_time import convert_string_to_date
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddBuilding(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        if property_id:
            return update_building(request)
        else:
            return create_building(request)


def create_building(request):
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")
    facing = json_to_python(request.POST.get("facing"))
    carpet_area = request.POST.get("carpet_area")
    land_size = request.POST.get("land_size")
    land_width = request.POST.get("land_width")
    land_length = request.POST.get("land_length")
    number_of_floors = request.POST.get("number_of_floors")
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    ready_to_occupy = json_to_python(request.POST.get("ready_to_occupy"))
    available_from = convert_string_to_date(request.POST.get("available_from"))
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
    sale_type = request.POST.get("sale_type")
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    bedroom_available = json_to_python(request.POST.get("bedroom_available"))
    about_property = request.POST.get("about_property")
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    contact_details = json_to_python(request.POST.get("contact_details"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects

    property_map, property_address, seller_contact = add_common_details(
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )

    property = Property.objects.create(
        project_name=project_name,
        seller=seller,
        final_price=float(final_price),
        property_type=PropertyTypes.Building,
        amenities=amenities,
        address=property_address,
        seller_contact=seller_contact,
        about_property=about_property,
    )

    Building.objects.create(
        property=property,
        facing=facing,
        land_size=land_size,
        land_width=land_width,
        land_length=land_length,
        carpet_area=carpet_area,
        number_of_floors=number_of_floors,
        number_of_car_parking=number_of_car_parking,
        number_of_bike_parking=number_of_bike_parking,
        ready_to_occupy=ready_to_occupy,
        available_from=available_from,
        sale_type=sale_type,
        furnishing_detail=furnishing_detail,
        bedroom_available=bedroom_available,
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


def update_building(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")
    facing = json_to_python(request.POST.get("facing"))
    carpet_area = request.POST.get("carpet_area")
    land_size = request.POST.get("land_size")
    land_width = request.POST.get("land_width")
    land_length = request.POST.get("land_length")
    number_of_floors = request.POST.get("number_of_floors")
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    ready_to_occupy = json_to_python(request.POST.get("ready_to_occupy"))
    available_from = convert_string_to_date(request.POST.get("available_from"))
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
    sale_type = request.POST.get("sale_type")
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    bedroom_available = json_to_python(request.POST.get("bedroom_available"))
    about_property = request.POST.get("about_property")
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    contact_details = json_to_python(request.POST.get("contact_details"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects

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
    property.property_type = PropertyTypes.Building
    property.amenities = amenities
    property.address = property_address
    property.seller_contact = seller_contact
    property.about_property = about_property
    property.updated_date = datetime.now()
    property.save()

    building = Building.objects.get(property=property)

    building.property = property
    building.facing = facing
    building.land_size = land_size
    building.land_width = land_width
    building.land_length = land_length
    building.carpet_area = carpet_area
    building.number_of_floors = number_of_floors
    building.number_of_car_parking = number_of_car_parking
    building.number_of_bike_parking = number_of_bike_parking
    building.ready_to_occupy = ready_to_occupy
    building.available_from = available_from
    building.sale_type = sale_type
    building.furnishing_detail = furnishing_detail
    building.bedroom_available = bedroom_available
    building.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )
    return send_pass_http_response({"property_id": property.id})
