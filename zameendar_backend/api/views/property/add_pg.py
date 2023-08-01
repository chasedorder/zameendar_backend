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
    PG,
    ContactDetails,
    Property,
    PropertyAddress,
    PropertyImage,
    PropertyMap,
    Seller,
)


class AddPG(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        project_name = request.POST["project_name"]

        address_details = json.loads(request.POST["address_detail"])  # json object
        final_price = request.POST["final_price"]
        sharing_for = request.POST["sharing_for"]
        sharing_type = request.POST["sharing_type"]
        price_per_month = request.POST["price_per_month"]
        advance_amount = request.POST["advance_amount"]
        attached_washroom = json.loads(request.POST["attached_washroom"])
        food_facility = json.loads(request.POST["food_facility"])
        parking_facility = json.loads(request.POST["parking_facility"])
        ready_to_move_in = json.loads(request.POST["ready_to_move_in"])
        other_facilities = json.loads(request.POST["other_facilities"])  # list of json objects

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

        PG.objects.create(
            property=property,
            sharing_type=sharing_type,
            sharing_for=sharing_for,
            attached_washroom=attached_washroom,
            food_facility=food_facility,
            parking_facility=parking_facility,
            price_per_month=float(price_per_month),
            advance_amount=float(advance_amount),
            other_facilities=other_facilities,
            ready_to_move_in=ready_to_move_in,
        )

        return send_pass_http_response({"message": "Property Added Successfully"})
