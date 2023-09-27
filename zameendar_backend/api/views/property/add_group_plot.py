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
from zameendar_backend.api.models import GroupPlot, Property, Seller
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddGroupPlot(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        if property_id:
            return update_group_plot(request)
        else:
            return create_group_plot(request)


def create_group_plot(request):
    project_name = request.POST.get("project_name")
    price_per_sqyd = request.POST.get("price_per_sqyd")
    start_price = request.POST.get("start_price")
    end_price = request.POST.get("end_price")
    plot_sizes = json.loads(request.POST.get("plot_sizes"))  # list of string
    total_project_area = request.POST.get("total_project_area")
    rera_id = request.POST.get("rera_id")
    facing = json_to_python(request.POST.get("facing"))
    address_details = json.loads(request.POST.get("address_detail"))  # json object
    amenities = json.loads(request.POST.get("amenities"))  # list of json objects
    maps_details = json.loads(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json.loads(request.POST.get("image_details"))  # list of json objects
    contact_details = json.loads(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")

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
        property_type=PropertyTypes.GroupPlot,
        address=property_address,
        amenities=amenities,
        seller_contact=seller_contact,
        map=property_map,
        about_property=about_property,
    )

    GroupPlot.objects.create(
        property=property,
        price_per_sqyd=price_per_sqyd,
        plot_sizes=plot_sizes,
        total_project_area=total_project_area,
        rera_id=rera_id,
        facing=facing,
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


def update_group_plot(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    price_per_sqyd = request.POST.get("price_per_sqyd")
    start_price = request.POST.get("start_price")
    end_price = request.POST.get("end_price")
    plot_sizes = json.loads(request.POST.get("plot_sizes"))  # list of string
    total_project_area = request.POST.get("total_project_area")
    rera_id = request.POST.get("rera_id")
    facing = json_to_python(request.POST.get("facing"))
    address_details = json.loads(request.POST.get("address_detail"))  # json object
    amenities = json.loads(request.POST.get("amenities"))  # list of json objects
    maps_details = json.loads(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json.loads(request.POST.get("image_details"))  # list of json objects
    contact_details = json.loads(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")

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
    property.property_type = PropertyTypes.GroupVilla
    property.about_property = about_property
    property.updated_date = datetime.now()
    property.save()

    group_plot = GroupPlot.objects.get(property=property)
    group_plot.property = property
    group_plot.price_per_sqyd = price_per_sqyd
    group_plot.plot_sizes = plot_sizes
    group_plot.total_project_area = total_project_area
    group_plot.rera_id = rera_id
    group_plot.facing = facing
    group_plot.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response({"property_id": property.id})
