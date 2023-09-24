import json

from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.meta_models import PropertyTypes
from zameendar_backend.api.models import (
    ContactDetails,
    GroupPlot,
    Property,
    PropertyAddress,
    PropertyImage,
    PropertyMap,
    Seller,
)
from zameendar_backend.api.utils.json_to_python import json_to_python


class AddGroupPlot(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
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

        property_address = PropertyAddress.objects.create(
            street_address=address_details.get("street_address"),
            area=address_details.get("area"),
            city=address_details["city"],
            state=address_details["state"],
            postal_code=address_details["postal_code"],
        )

        seller_contact = ContactDetails.objects.create(
            phone_number_1=contact_details["phone_number_1"],
            phone_number_2=contact_details["phone_number_2"],
            email=contact_details["email"],
        )

        if maps_details:
            property_map = PropertyMap.objects.create(location=maps_details.get("location"))
        else:
            property_map = None

        property = Property.objects.create(
            project_name=project_name,
            seller=seller,
            start_price=float(start_price),
            end_price=float(end_price),
            property_type=PropertyTypes.GroupPlot,
            address=property_address,
            amenities=amenities,
            seller_contact=seller_contact,
            map=property_map,
            about_property=about_property,
        )

        property_images_obj_list = []
        for image, image_detail in zip(property_images, image_details):
            property_images_obj_list.append(
                PropertyImage(
                    title=image_detail["title"],
                    property=property,
                    meta_data=image_detail["meta_data"],
                    image=image,
                )
            )
        PropertyImage.objects.bulk_create(property_images_obj_list)

        GroupPlot.objects.create(
            property=property,
            price_per_sqyd=float(price_per_sqyd),
            plot_sizes=plot_sizes,
            total_project_area=total_project_area,
            rera_id=rera_id,
            facing=facing,
        )

        return send_pass_http_response({"message": "Property Added Successfully"})
