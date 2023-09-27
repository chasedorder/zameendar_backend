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
from zameendar_backend.api.models import GroupVilla, Property, Seller
from zameendar_backend.api.utils.formatting_date_time import formatting_date
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddGroupVilla(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        if property_id:
            return update_group_villa(request)
        else:
            return create_group_villa(request)


def update_group_villa(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    price_per_sqft = request.POST.get("price_per_sqft")
    start_price = request.POST.get("start_price")
    end_price = request.POST.get("end_price")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    bhk_details = json_to_python(request.POST.get("bhk_details"))  # list of json objects
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
    land_area_sizes = json_to_python(request.POST.get("land_area_sizes"))  # list of string
    land_width = request.POST.get("land_width")
    land_length = request.POST.get("land_length")
    number_of_floors = json_to_python(request.POST.get("number_of_floors"))  # list of string
    ready_to_occupy = json_to_python(request.POST.get("ready_to_occupy"))  # false or true
    about_property = request.POST.get("about_property")
    if not ready_to_occupy:
        possession_date = formatting_date(request.POST.get("possession_date"))
    else:
        possession_date = None
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    total_project_area = request.POST.get("total_project_area")
    rera_id = request.POST.get("rera_id")
    facing = json_to_python(request.POST.get("facing"))
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    project_size = request.POST.get("project_size")
    sale_type = request.POST.get("sale_type")
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
    property.start_price = float(start_price)
    property.end_price = float(end_price)
    property.seller = seller
    property.amenities = amenities
    property.address = property_address
    property.seller_contact = seller_contact
    property.map = property_map
    property.property_type = PropertyTypes.GroupVilla
    property.about_property = about_property
    property.updated_date = datetime.now()
    property.save()

    group_villa = GroupVilla.objects.get(property=property)
    group_villa.property = property
    group_villa.price_per_sqft = price_per_sqft
    group_villa.bhk_details = bhk_details
    group_villa.land_area_sizes = land_area_sizes
    group_villa.number_of_floors = number_of_floors
    group_villa.land_width = land_width
    group_villa.land_length = land_length
    group_villa.ready_to_occupy = ready_to_occupy
    group_villa.possession_date = possession_date
    group_villa.number_of_car_parking = number_of_car_parking
    group_villa.number_of_bike_parking = number_of_bike_parking
    group_villa.total_project_area = total_project_area
    group_villa.rera_id = rera_id
    group_villa.facing = facing
    group_villa.furnishing_detail = furnishing_detail
    group_villa.project_size = project_size
    group_villa.sale_type = sale_type
    group_villa.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response({"property_id": property.id})


def create_group_villa(request):
    project_name = request.POST.get("project_name")
    price_per_sqft = request.POST.get("price_per_sqft")
    start_price = request.POST.get("start_price")
    end_price = request.POST.get("end_price")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    bhk_details = json_to_python(request.POST.get("bhk_details"))  # list of json objects
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
    land_area_sizes = json_to_python(request.POST.get("land_area_sizes"))  # list of string
    land_width = request.POST.get("land_width")
    land_length = request.POST.get("land_length")
    number_of_floors = json_to_python(request.POST.get("number_of_floors"))  # list of string
    ready_to_occupy = json_to_python(request.POST.get("ready_to_occupy"))  # false or true
    about_property = request.POST.get("about_property")
    if not ready_to_occupy:
        possession_date = formatting_date(request.POST.get("possession_date"))
    else:
        possession_date = None
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    total_project_area = request.POST.get("total_project_area")
    rera_id = request.POST.get("rera_id")
    facing = json_to_python(request.POST.get("facing"))
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    project_size = request.POST.get("project_size")
    sale_type = request.POST.get("sale_type")
    seller = Seller.objects.get(user=request.user)
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
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
        start_price=start_price,
        end_price=end_price,
        property_type=PropertyTypes.GroupVilla,
        amenities=amenities,
        address=property_address,
        seller_contact=seller_contact,
        map=property_map,
        about_property=about_property,
    )

    GroupVilla.objects.create(
        property=property,
        price_per_sqft=price_per_sqft,
        bhk_details=bhk_details,
        land_area_sizes=land_area_sizes,
        number_of_floors=number_of_floors,
        land_width=land_width,
        land_length=land_length,
        ready_to_occupy=ready_to_occupy,
        possession_date=possession_date,
        number_of_car_parking=int(number_of_car_parking),
        number_of_bike_parking=int(number_of_bike_parking),
        total_project_area=total_project_area,
        rera_id=rera_id,
        facing=facing,
        furnishing_detail=furnishing_detail,
        project_size=project_size,
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
