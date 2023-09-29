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
from zameendar_backend.api.models import GroupAppartment, Property, Seller
from zameendar_backend.api.utils.formatting_date_time import convert_string_to_date
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddGroupAppartment(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        # for updating
        if property_id:
            return update_group_appartment(request)
        # for adding new
        else:
            return create_group_appartment(request)


def create_group_appartment(request):
    project_name = request.POST.get("project_name")

    price_per_sqft = request.POST.get("price_per_sqft")
    start_price = request.POST.get("start_price")
    end_price = request.POST.get("end_price")

    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    bhk_details = json_to_python(request.POST.get("bhk_details"))  # list of json objects
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects

    number_of_floors = request.POST.get("number_of_floors")
    ready_to_occupy = json_to_python(request.POST.get("ready_to_occupy", "false"))  # false or true
    if not ready_to_occupy:
        possession_date = convert_string_to_date(request.POST.get("possession_date"))
    else:
        possession_date = None

    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    project_area = request.POST.get("project_area")
    project_size = request.POST.get("project_size")
    rera_id = request.POST.get("rera_id")
    sale_type = request.POST.get("sale_type")
    property_age = request.POST.get("property_age")
    number_of_bedrooms = request.POST.get("number_of_bedrooms")
    number_of_bathrooms = request.POST.get("number_of_bathrooms")
    facing = json_to_python(request.POST.get("facing"))
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    maps_details = json_to_python(request.POST.get("maps_details", "false"))  # json object
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")

    property_map, property_address, seller_contact = add_common_details(
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )

    property = Property.objects.create(
        project_name=project_name,
        start_price=start_price,
        end_price=end_price,
        seller=seller,
        property_type=PropertyTypes.GroupAppart,
        amenities=amenities,
        address=property_address,
        seller_contact=seller_contact,
        map=property_map,
        about_property=about_property,
    )

    GroupAppartment.objects.create(
        property=property,
        price_per_sqft=price_per_sqft,
        bhk_details=bhk_details,
        number_of_floors=number_of_floors,
        ready_to_occupy=ready_to_occupy,
        possession_date=possession_date,
        number_of_car_parking=number_of_car_parking,
        number_of_bike_parking=number_of_bike_parking,
        project_area=project_area,
        project_size=project_size,
        rera_id=rera_id,
        sale_type=sale_type,
        property_age=property_age,
        number_of_bedrooms=number_of_bedrooms,
        number_of_bathrooms=number_of_bathrooms,
        facing=facing,
        furnishing_detail=furnishing_detail,
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


def update_group_appartment(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    price_per_sqft = request.POST.get("price_per_sqft")
    start_price = request.POST.get("start_price")
    end_price = request.POST.get("end_price")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    bhk_details = json_to_python(request.POST.get("bhk_details"))  # list of json objects
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
    number_of_floors = request.POST.get("number_of_floors")
    ready_to_occupy = json_to_python(request.POST.get("ready_to_occupy", "false"))  # false or true
    number_of_car_parking = request.POST.get("number_of_car_parking")
    number_of_bike_parking = request.POST.get("number_of_bike_parking")
    project_area = request.POST.get("project_area")
    project_size = request.POST.get("project_size")
    rera_id = request.POST.get("rera_id")
    sale_type = request.POST.get("sale_type")
    property_age = request.POST.get("property_age")
    number_of_bedrooms = request.POST.get("number_of_bedrooms")
    number_of_bathrooms = request.POST.get("number_of_bathrooms")
    facing = json_to_python(request.POST.get("facing"))
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    maps_details = json_to_python(request.POST.get("maps_details", "false"))  # json object
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")

    if not ready_to_occupy:
        possession_date = convert_string_to_date(request.POST.get("possession_date"))
    else:
        possession_date = None

    property = Property.objects.get(id=property_id)

    property_map, property_address, seller_contact = update_common_details(
        property=property,
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )

    property.project_name = project_name
    property.start_price = start_price
    property.end_price = end_price
    property.seller = seller
    property.amenities = amenities
    property.address = property_address
    property.seller_contact = seller_contact
    property.map = property_map
    property.property_type = PropertyTypes.GroupAppart
    property.about_property = about_property
    property.updated_date = datetime.now()
    property.save()

    group_appartment = GroupAppartment.objects.get(property=property)
    group_appartment.property = property
    group_appartment.price_per_sqft = price_per_sqft
    group_appartment.bhk_details = bhk_details
    group_appartment.number_of_floors = number_of_floors
    group_appartment.ready_to_occupy = ready_to_occupy
    group_appartment.possession_date = possession_date
    group_appartment.number_of_car_parking = number_of_car_parking
    group_appartment.number_of_bike_parking = number_of_bike_parking
    group_appartment.project_area = project_area
    group_appartment.project_size = project_size
    group_appartment.rera_id = rera_id
    group_appartment.sale_type = sale_type
    group_appartment.property_age = property_age
    group_appartment.number_of_bedrooms = number_of_bedrooms
    group_appartment.number_of_bathrooms = number_of_bathrooms
    group_appartment.facing = facing
    group_appartment.furnishing_detail = furnishing_detail
    group_appartment.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response({"property_id": property.id})
