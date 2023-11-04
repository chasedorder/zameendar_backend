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
from zameendar_backend.api.models import OpenPlot, PropertyModel, Seller
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property_utils.add_common_details import add_common_details
from zameendar_backend.api.utils.property_utils.add_property_images import add_property_images
from zameendar_backend.api.utils.property_utils.update_common_details import update_common_details


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

    property_model = PropertyModel.objects.create(
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
        property_model=property_model,
        facing=facing,
        land_size=land_size,
        land_width=land_width,
        land_length=land_length,
        is_fencing=is_fencing,
        price_per_square_yard=price_per_square_yard,
    )

    if image_details:
        add_property_images(
            property_model=property_model,
            property_images=property_images,
            image_details=image_details,
        )

    return send_pass_http_response(
        {
            "message": "Property Added Successfully",
            "property_id": property_model.id,
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

    property_model = PropertyModel.objects.get(id=property_id)

    property_map, property_address, seller_contact = update_common_details(
        property_model=property_model,
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )

    property_model.project_name = project_name
    property_model.seller = seller
    property_model.final_price = final_price
    property_model.property_type = PropertyTypes.OpenPlot
    property_model.address = property_address
    property_model.seller_contact = seller_contact
    property_model.map = property_map
    property_model.about_property = about_property
    property_model.amenities = amenities
    property_model.updated_date = datetime.now()
    property_model.current_step = current_step
    property_model.save()

    open_plot = OpenPlot.objects.get(property_model=property_model)
    open_plot.property_model = property_model
    open_plot.facing = facing
    open_plot.land_size = land_size
    open_plot.land_width = land_width
    open_plot.land_length = land_length
    open_plot.is_fencing = is_fencing
    open_plot.price_per_square_yard = price_per_square_yard
    open_plot.save()

    if image_details:
        add_property_images(
            property_model=property_model,
            property_images=property_images,
            image_details=image_details,
        )

    return send_pass_http_response({"property_id": property_model.id})
