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
    Flat,
    Property,
    PropertyAddress,
    PropertyImage,
    PropertyMap,
    Seller,
)
from zameendar_backend.api.utils.formatting_date_time import formatting_date


class AddFlat(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        project_name = request.POST["project_name"]

        address_details = json.loads(request.POST["address_detail"])  # json object
        final_price = request.POST["final_price"]
        facing = request.POST["facing"]
        carpet_area = request.POST["carpet_area"]
        bedroom_available = json.loads(request.POST["bedroom_available"])  # list of string
        number_of_washrooms = request.POST["number_of_washrooms"]
        floor_number = request.POST["floor_number"]
        number_of_car_parking = request.POST["number_of_car_parking"]
        number_of_bike_parking = request.POST["number_of_bike_parking"]
        furnishing_detail = json.loads(request.POST["furnishing_detail"])  # list of string
        ready_to_occupy = json.loads(request.POST["ready_to_occupy"])
        available_from = formatting_date(request.POST["available_from"])

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

        property_address = PropertyAddress.objects.create(
            street_address=address_details.get("street_address"),
            area=address_details.get("area"),
            city=address_details["city"],
            state=address_details["state"],
            postal_code=address_details["postal_code"],
        )
        property = Property.objects.create(
            project_name=project_name,
            seller=seller,
            final_price=float(final_price),
            property_type=Property.GroupAppart,
            amenities=amenities,
            address=property_address,
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

        Flat.objects.create(
            property=property,
            facing=facing,
            carpet_area=carpet_area,
            bedroom_available=bedroom_available,
            number_of_washrooms=int(number_of_washrooms),
            floor_number=int(floor_number),
            number_of_car_parking=int(number_of_car_parking),
            number_of_bike_parking=int(number_of_bike_parking),
            furnishing_detail=furnishing_detail,
            ready_to_occupy=ready_to_occupy,
            available_from=available_from,
        )

        return send_pass_http_response({"message": "Property Added Successfully"})
