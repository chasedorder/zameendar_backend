import json

from rest_framework import authentication, permissions
from rest_framework.views import APIView

from zameendar_backend.api.dispatchers.responses.send_fail_http_response import (
    send_fail_http_response,
)
from zameendar_backend.api.dispatchers.responses.send_pass_http_response import (
    send_pass_http_response,
)
from zameendar_backend.api.models import (
    ContactDetails,
    GroupPlot,
    Property,
    PropertyImage,
    PropertyMap,
    Seller,
)


class AddGroupPlot(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        project_name = request.POST["project_name"]

        price_per_sqyd = request.POST["price_per_sqyd"]
        start_price = request.POST["start_price"]
        end_price = request.POST["end_price"]
        plot_size = request.POST["plot_size"]

        amenities = json.loads(request.POST["amenities"])  # list of json objects

        maps_details = json.loads(request.POST.get("maps_details", "false"))

        seller = Seller.objects.get(user=request.user)

        property_images = request.FILES.getlists("property_images")
        image_details = json.loads(request.POST.get("images_date", "false"))  # list of json objects

        contact_details = json.loads(request.POST["contact_details"])

        seller_contact = ContactDetails.objects.create(
            phone_number_1=contact_details["phone_number_1"],
            phone_number_2=contact_details["phone_number_2"],
            email=contact_details["email"],
        )

        if maps_details:
            property_map = PropertyMap.objects.create(location=request.POST["location"])
        else:
            property_map = None

        property = Property.objects.create(
            project_name=project_name,
            seller=seller,
            start_price=float(start_price),
            end_price=float(end_price),
            property_type=Property.GroupAppart,
            amenities=amenities,
            seller_contact=seller_contact,
            map=property_map,
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
            plot_size=float(plot_size),
        )

        return send_pass_http_response({"message": "Property Added Successfully"})
