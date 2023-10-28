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
from zameendar_backend.api.models import OpenPlot, Property, Seller
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddOpenPlot(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        if property_id:
            return update_open_plot(request)
        else:
            return create_open_plot(request)


def create_open_plot(request):
    project_name = request.POST.get("project_name")

    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")

    facing = json_to_python(request.POST.get("facing"))
    land_size = request.POST.get("land_size")
    land_width = request.POST.get("land_width")
    land_length = request.POST.get("land_length")
    is_fencing = json_to_python(request.POST.get("is_fencing"))
    price_per_square_yard = request.POST.get("price_per_square_yard")
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
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
        property_type=PropertyTypes.OpenPlot,
        address=property_address,
        seller_contact=seller_contact,
        map=property_map,
        amenities=amenities,
        about_property=about_property,
        current_step=current_step,
    )

    OpenPlot.objects.create(
        property=property,
        facing=facing,
        land_size=land_size,
        land_width=land_width,
        land_length=land_length,
        is_fencing=is_fencing,
        price_per_square_yard=price_per_square_yard,
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


def update_open_plot(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")
    facing = json_to_python(request.POST.get("facing"))
    land_size = request.POST.get("land_size")
    land_width = request.POST.get("land_width")
    land_length = request.POST.get("land_length")
    is_fencing = json_to_python(request.POST.get("is_fencing"))
    price_per_square_yard = request.POST.get("price_per_square_yard")
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")
    amenities = json_to_python(request.POST.get("amenities"))  # list of json objects
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
    property.property_type = PropertyTypes.OpenPlot
    property.address = property_address
    property.seller_contact = seller_contact
    property.map = property_map
    property.about_property = about_property
    property.amenities = amenities
    property.updated_date = datetime.now()
    property.current_step = current_step
    property.save()

    open_plot = OpenPlot.objects.get(property=property)
    open_plot.property = property
    open_plot.facing = facing
    open_plot.land_size = land_size
    open_plot.land_width = land_width
    open_plot.land_length = land_length
    open_plot.is_fencing = is_fencing
    open_plot.price_per_square_yard = price_per_square_yard
    open_plot.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response({"property_id": property.id})
