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
    GroupAppartment,
    Property,
    PropertyAddress,
    PropertyImage,
    PropertyMap,
    Seller,
)
from zameendar_backend.api.utils.formatting_date_time import formatting_date


class AddGroupAppartment(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        project_name = request.POST["project_name"]

        price_per_sqft = request.POST["price_per_sqft"]
        start_price = request.POST["start_price"]
        end_price = request.POST["end_price"]

        address_details = json.loads(request.POST["address_detail"])  # json object
        bhk_details = json.loads(request.POST["bhk_details"])  # list of json objects
        amenities = json.loads(request.POST["amenities"])  # list of json objects

        number_of_floors = request.POST["number_of_floors"]
        ready_to_occupy = json.loads(request.POST["ready_to_occupy"])  # false or true
        if not ready_to_occupy:
            possession_date = formatting_date(request.POST["possession_date"])
        else:
            possession_date = None

        number_of_car_parking = request.POST["number_of_car_parking"]
        number_of_bike_parking = request.POST["number_of_bike_parking"]

        maps_details = json.loads(request.POST.get("maps_details", "false"))  # json object

        seller = Seller.objects.get(user=request.user)

        property_images = request.FILES.getlist("property_images")
        image_details = json.loads(
            request.POST.get("image_details", "false")
        )  # list of json objects

        property_address = PropertyAddress.objects.create(
            street_address=address_details.get("street_address"),
            area=address_details.get("area"),
            city=address_details["city"],
            state=address_details["state"],
            postal_code=address_details["postal_code"],
        )

        contact_details = json.loads(request.POST["contact_details"])

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
            start_price=float(start_price),
            end_price=float(end_price),
            seller=seller,
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

        GroupAppartment.objects.create(
            property=property,
            price_per_sqft=float(price_per_sqft),
            bhk_details=bhk_details,
            number_of_floors=int(number_of_floors),
            ready_to_occupy=ready_to_occupy,
            possession_date=possession_date,
            number_of_car_parking=int(number_of_car_parking),
            number_of_bike_parking=int(number_of_bike_parking),
        )

        return send_pass_http_response({"message": "Property Added Successfully"})
