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
    Property,
    PropertyAddress,
    PropertyImage,
    PropertyMap,
    Rent,
    Seller,
)


class AddRent(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        project_name = request.POST["project_name"]

        address_details = json.loads(request.POST["address_detail"])  # json object
        facing = json.loads(request.POST["facing"])
        rent_per_month = request.POST["rent_per_month"]
        advance_amount = request.POST["advance_amount"]
        floor_number = request.POST["floor_number"]
        number_of_car_parking = request.POST["number_of_car_parking"]
        number_of_bike_parking = request.POST["number_of_bike_parking"]
        furnishing_detail = request.POST["furnishing_detail"]
        ready_to_occupy = json.loads(request.POST["ready_to_occupy"])

        maps_details = json.loads(request.POST.get("maps_details", "false"))

        seller = Seller.objects.get(user=request.user)

        property_images = request.FILES.getlist("property_images")
        image_details = json.loads(
            request.POST.get("image_details", "false")
        )  # list of json objects

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
            property_type=PropertyTypes.Rent,
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

        Rent.objects.create(
            property=property,
            facing=facing,
            floor_number=int(floor_number),
            number_of_car_parking=int(number_of_car_parking),
            number_of_bike_parking=int(number_of_bike_parking),
            furnishing_detail=furnishing_detail,
            ready_to_move_in=ready_to_occupy,
            rent_per_month=float(rent_per_month),
            advance_amount=float(advance_amount),
        )

        return send_pass_http_response({"message": "Property Added Successfully"})
