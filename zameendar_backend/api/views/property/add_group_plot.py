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
from zameendar_backend.api.models import GroupPlot, PropertyModel, Seller
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property_utils.add_common_details import add_common_details
from zameendar_backend.api.utils.property_utils.add_property_images import add_property_images
from zameendar_backend.api.utils.property_utils.update_common_details import update_common_details


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
    current_step = int(request.POST.get("current_step", 0))

    property_map, property_address, seller_contact = add_common_details(
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )
    property_model = PropertyModel.objects.create(
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
        current_step=current_step,
    )

    GroupPlot.objects.create(
        property_model=property_model,
        price_per_sqyd=price_per_sqyd,
        plot_sizes=plot_sizes,
        total_project_area=total_project_area,
        rera_id=rera_id,
        facing=facing,
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
    current_step = int(request.POST.get("current_step", 0))

    property_model = PropertyModel.objects.get(id=property_id)

    property_map, property_address, seller_contact = update_common_details(
        property_model=property_model,
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )

    property_model.project_name = project_name
    property_model.start_price = start_price
    property_model.end_price = end_price
    property_model.seller = seller
    property_model.amenities = amenities
    property_model.address = property_address
    property_model.seller_contact = seller_contact
    property_model.map = property_map
    property_model.property_type = PropertyTypes.GroupPlot
    property_model.about_property = about_property
    property_model.updated_date = datetime.now()
    property_model.current_step = current_step
    property_model.save()

    group_plot = GroupPlot.objects.get(property_model=property_model)
    group_plot.property_model = property_model
    group_plot.price_per_sqyd = price_per_sqyd
    group_plot.plot_sizes = plot_sizes
    group_plot.total_project_area = total_project_area
    group_plot.rera_id = rera_id
    group_plot.facing = facing
    group_plot.save()

    if image_details:
        add_property_images(
            property_model=property_model,
            property_images=property_images,
            image_details=image_details,
        )

    return send_pass_http_response({"property_id": property_model.id})
