import json
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
from zameendar_backend.api.models import Property, Rent, Seller
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddRent(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        # for updating
        if property_id:
            return update_rent(request)
        # for adding new
        else:
            return create_rent(request)


def create_rent(request):
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    rent_type = request.POST.get("rent_type")
    facing = json_to_python(request.POST.get("facing"))
    rent_per_month = request.POST.get("rent_per_month")
    advance_amount = request.POST.get("advance_amount")
    floor_number = request.POST.get("floor_number")
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    ready_to_move_in = json_to_python(request.POST.get("ready_to_move_in"))
    carpet_area = request.POST.get("carpet_area")
    bedroom_available = json_to_python(request.POST.get("bedroom_available"))
    about_property = request.POST.get("about_property")
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))

    property_map, property_address, seller_contact = add_common_details(
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )
    property = Property.objects.create(
        project_name=project_name,
        seller=seller,
        property_type=PropertyTypes.Rent,
        address=property_address,
        seller_contact=seller_contact,
        map=property_map,
        about_property=about_property,
    )

    Rent.objects.create(
        property=property,
        rent_type=rent_type,
        facing=facing,
        floor_number=floor_number,
        number_of_car_parking=number_of_car_parking,
        number_of_bike_parking=number_of_bike_parking,
        furnishing_detail=furnishing_detail,
        ready_to_move_in=ready_to_move_in,
        rent_per_month=rent_per_month,
        advance_amount=advance_amount,
        carpet_area=carpet_area,
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


def update_rent(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    facing = json_to_python(request.POST.get("facing"))
    rent_per_month = request.POST.get("rent_per_month")
    advance_amount = request.POST.get("advance_amount")
    floor_number = request.POST.get("floor_number")
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    ready_to_move_in = json_to_python(request.POST.get("ready_to_move_in"))
    carpet_area = request.POST.get("carpet_area")
    bedroom_available = json_to_python(request.POST.get("bedroom_available"))
    about_property = request.POST.get("about_property")
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))

    property = Property.objects.get(id=property_id)

    property_map, property_address, seller_contact = update_common_details(
        property=property,
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )
    property.project_name = project_name
    property.seller = seller
    property.property_type = PropertyTypes.Rent
    property.address = property_address
    property.seller_contact = seller_contact
    property.map = property_map
    property.about_property = about_property
    property.updated_date = datetime.now()
    property.save()

    rent = Rent.objects.get(property=property)
    rent.property = property
    rent.facing = facing
    rent.floor_number = floor_number
    rent.number_of_car_parking = number_of_car_parking
    rent.number_of_bike_parking = number_of_bike_parking
    rent.furnishing_detail = furnishing_detail
    rent.ready_to_move_in = ready_to_move_in
    rent.rent_per_month = rent_per_month
    rent.advance_amount = advance_amount
    rent.carpet_area = carpet_area
    rent.bedroom_available = bedroom_available

    rent.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response({"property_id": property.id})
