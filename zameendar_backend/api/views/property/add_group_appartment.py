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
        property_id = request.POST.get("property_id")

        project_name = request.POST.get("project_name")

        price_per_sqft = request.POST.get("price_per_sqft")
        start_price = request.POST.get("start_price")
        end_price = request.POST.get("end_price")

        address_details = json.loads(request.POST.get("address_detail", "{}"))  # json object
        bhk_details = json.loads(request.POST.get("bhk_details", "[]"))  # list of json objects
        amenities = json.loads(request.POST.get("amenities", "[]"))  # list of json objects

        number_of_floors = request.POST.get("number_of_floors")
        ready_to_occupy = json.loads(request.POST.get("ready_to_occupy", "false"))  # false or true
        if not ready_to_occupy:
            possession_date = formatting_date(request.POST.get("possession_date"))
        else:
            possession_date = None

        number_of_car_parking = request.POST.get("number_of_car_parking")
        number_of_bike_parking = request.POST.get("number_of_bike_parking")
        project_area = request.POST.get("project_area")
        project_size = request.POST.get("project_size")
        rera_id = request.POST.get("rera_id")
        sale_type = request.POST.get("sale_type")
        property_age = request.POST.get("property_age")
        number_of_bedrooms = request.POST.get("number_of_bedrooms")
        number_of_bathrooms = request.POST.get("number_of_bathrooms")
        facing = json.loads(request.POST.get("facing", "[]"))
        furnishing_detail = json.loads(request.POST.get("furnishing_detail", "[]"))
        maps_details = json.loads(request.POST.get("maps_details", "false"))  # json object

        seller = Seller.objects.get(user=request.user)

        property_images = request.FILES.getlist("property_images")
        image_details = json.loads(
            request.POST.get("image_details", "false")
        )  # list of json objects
        contact_details = json.loads(request.POST.get("contact_details", "{}"))

        about_property = request.POST.get("about_property")

        # for updating
        if property_id:
            property = Property.objects.get(id=property_id)
            property_map = None
            if maps_details:
                property_map = property.map
                if property_map:
                    property_map.location = maps_details.get("location")
                    property_map.save()
                else:
                    property_map = PropertyMap.objects.create(location=maps_details.get("location"))
            if address_details:
                property_address = property.address
                if property_address:
                    property_address.street_address = address_details.get("street_address")
                    property_address.area = address_details.get("area")
                    property_address.city = address_details["city"]
                    property_address.state = address_details["state"]
                    property_address.postal_code = address_details["postal_code"]
                    property_address.save()
                else:
                    property_address = PropertyAddress.objects.create(
                        street_address=address_details.get("street_address"),
                        area=address_details.get("area"),
                        city=address_details["city"],
                        state=address_details["state"],
                        postal_code=address_details["postal_code"],
                    )
            if contact_details:
                seller_contact = property.seller_contact
                if seller_contact:
                    seller_contact.street_address = address_details.get("street_address")
                    seller_contact.area = address_details.get("area")
                    seller_contact.city = address_details["city"]
                    seller_contact.state = address_details["state"]
                    seller_contact.postal_code = address_details["postal_code"]
                    seller_contact.save()
                else:
                    seller_contact = ContactDetails.objects.create(
                        phone_number_1=contact_details["phone_number_1"],
                        phone_number_2=contact_details["phone_number_2"],
                        email=contact_details["email"],
                    )

            property.project_name = project_name
            property.start_price = float(start_price)
            property.end_price = float(end_price)
            property.seller = seller
            property.amenities = amenities
            property.address = property_address
            property.seller_contact = seller_contact
            property.map = property_map
            property.property_type = PropertyTypes.GroupAppart
            property.about_property = about_property
            property.updated_date = datetime.now()
            property.save()

            group_appartment = GroupAppartment.objects.get(property=property)
            group_appartment.property = property
            group_appartment.price_per_sqft = price_per_sqft
            group_appartment.bhk_details = bhk_details
            group_appartment.number_of_floors = number_of_floors
            group_appartment.ready_to_occupy = ready_to_occupy
            group_appartment.possession_date = possession_date
            group_appartment.number_of_car_parking = number_of_car_parking
            group_appartment.number_of_bike_parking = number_of_bike_parking
            group_appartment.project_area = project_area
            group_appartment.project_size = project_size
            group_appartment.rera_id = rera_id
            group_appartment.sale_type = sale_type
            group_appartment.property_age = property_age
            group_appartment.number_of_bedrooms = number_of_bedrooms
            group_appartment.number_of_bathrooms = number_of_bathrooms
            group_appartment.facing = facing
            group_appartment.furnishing_detail = furnishing_detail

            group_appartment.save()

            return send_pass_http_response({"property_id": property.id})

        # for adding new
        else:
            if address_details:
                property_address = PropertyAddress.objects.create(
                    street_address=address_details.get("street_address"),
                    area=address_details.get("area"),
                    city=address_details["city"],
                    state=address_details["state"],
                    postal_code=address_details["postal_code"],
                )
            else:
                property_address = None

            if contact_details:
                seller_contact = ContactDetails.objects.create(
                    phone_number_1=contact_details["phone_number_1"],
                    phone_number_2=contact_details["phone_number_2"],
                    email=contact_details["email"],
                )
            else:
                seller_contact = None
            if maps_details:
                property_map = PropertyMap.objects.create(location=maps_details.get("location"))
            else:
                property_map = None

            property = Property.objects.create(
                project_name=project_name,
                start_price=start_price,
                end_price=end_price,
                seller=seller,
                property_type=PropertyTypes.GroupAppart,
                amenities=amenities,
                address=property_address,
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

            GroupAppartment.objects.create(
                property=property,
                price_per_sqft=price_per_sqft,
                bhk_details=bhk_details,
                number_of_floors=number_of_floors,
                ready_to_occupy=ready_to_occupy,
                possession_date=possession_date,
                number_of_car_parking=number_of_car_parking,
                number_of_bike_parking=number_of_bike_parking,
                project_area=project_area,
                project_size=project_size,
                rera_id=rera_id,
                sale_type=sale_type,
                property_age=property_age,
                number_of_bedrooms=number_of_bedrooms,
                number_of_bathrooms=number_of_bathrooms,
                facing=facing,
                furnishing_detail=furnishing_detail,
            )

            return send_pass_http_response(
                {
                    "message": "Property Added Successfully",
                    "property_id": property.id,
                }
            )
