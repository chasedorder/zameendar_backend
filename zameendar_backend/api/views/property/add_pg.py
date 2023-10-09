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
from zameendar_backend.api.models import PG, Property, Seller
from zameendar_backend.api.utils.json_to_python import json_to_python
from zameendar_backend.api.utils.property.add_common_details import add_common_details
from zameendar_backend.api.utils.property.add_property_images import add_property_images
from zameendar_backend.api.utils.property.update_common_details import update_common_details


class AddPG(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        property_id = request.POST.get("property_id")

        # for updating
        if property_id:
            return update_pg(request)
        # for adding new
        else:
            return create_pg(request)


def create_pg(request):
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")
    sharing_for = json_to_python(request.POST.get("sharing_for"))
    sharing_types = json_to_python(request.POST.get("sharing_types"))
    attached_washroom = json_to_python(request.POST.get("attached_washroom"))
    food_facility = json_to_python(request.POST.get("food_facility"))
    parking_facility = json_to_python(request.POST.get("parking_facility"))
    ready_to_move_in = json_to_python(request.POST.get("ready_to_move_in"))
    other_facilities = json_to_python(request.POST.get("other_facilities"))  # list of json objects
    coliving_common_areas = json_to_python(request.POST.get("coliving_common_areas"))
    non_veg_available = json_to_python(request.POST.get("non_veg_available"))
    visitor_allowed = json_to_python(request.POST.get("visitor_allowed"))
    opposite_sex_visitor_allowed = json_to_python(request.POST.get("opposite_sex_visitor_allowed"))
    drinking_allowed = json_to_python(request.POST.get("drinking_allowed"))
    smoking_allowed = json_to_python(request.POST.get("smoking_allowed"))
    any_time_allowed = json_to_python(request.POST.get("any_time_allowed"))
    last_time_entry = json_to_python(request.POST.get("last_time_entry"))
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    food_offerings = json_to_python(request.POST.get("food_offerings"))
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")

    property_map, property_address, seller_contact = add_common_details(
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )
    property = Property.objects.create(
        project_name=project_name,
        seller=seller,
        final_price=final_price,
        property_type=PropertyTypes.PG,
        address=property_address,
        seller_contact=seller_contact,
        map=property_map,
        about_property=about_property,
    )

    PG.objects.create(
        property=property,
        sharing_types=sharing_types,
        sharing_for=sharing_for,
        attached_washroom=attached_washroom,
        food_facility=food_facility,
        parking_facility=parking_facility,
        other_facilities=other_facilities,
        ready_to_move_in=ready_to_move_in,
        coliving_common_areas=coliving_common_areas,
        non_veg_available=non_veg_available,
        visitor_allowed=visitor_allowed,
        opposite_sex_visitor_allowed=opposite_sex_visitor_allowed,
        drinking_allowed=drinking_allowed,
        smoking_allowed=smoking_allowed,
        any_time_allowed=any_time_allowed,
        last_time_entry=last_time_entry,
        furnishing_detail=furnishing_detail,
        food_offerings=food_offerings,
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


def update_pg(request):
    property_id = request.POST.get("property_id")
    project_name = request.POST.get("project_name")
    address_details = json_to_python(request.POST.get("address_detail"))  # json object
    final_price = request.POST.get("final_price")
    sharing_for = json_to_python(request.POST.get("sharing_for"))
    sharing_types = json_to_python(request.POST.get("sharing_types"))
    attached_washroom = json_to_python(request.POST.get("attached_washroom"))
    food_facility = json_to_python(request.POST.get("food_facility"))
    parking_facility = json_to_python(request.POST.get("parking_facility"))
    ready_to_move_in = json_to_python(request.POST.get("ready_to_move_in"))
    other_facilities = json_to_python(request.POST.get("other_facilities"))  # list of json objects
    coliving_common_areas = json_to_python(request.POST.get("coliving_common_areas"))
    non_veg_available = json_to_python(request.POST.get("non_veg_available"))
    visitor_allowed = json_to_python(request.POST.get("visitor_allowed"))
    opposite_sex_visitor_allowed = json_to_python(request.POST.get("opposite_sex_visitor_allowed"))
    drinking_allowed = json_to_python(request.POST.get("drinking_allowed"))
    smoking_allowed = json_to_python(request.POST.get("smoking_allowed"))
    any_time_allowed = json_to_python(request.POST.get("any_time_allowed"))
    last_time_entry = json_to_python(request.POST.get("last_time_entry"))
    furnishing_detail = json_to_python(request.POST.get("furnishing_detail"))
    food_offerings = json_to_python(request.POST.get("food_offerings"))
    maps_details = json_to_python(request.POST.get("maps_details", "false"))
    seller = Seller.objects.get(user=request.user)
    property_images = request.FILES.getlist("property_images")
    image_details = json_to_python(request.POST.get("image_details"))  # list of json objects
    contact_details = json_to_python(request.POST.get("contact_details"))
    about_property = request.POST.get("about_property")

    property = Property.objects.get(id=property_id)

    property_map, property_address, seller_contact = update_common_details(
        property=property,
        maps_details=maps_details,
        address_details=address_details,
        contact_details=contact_details,
    )

    property.project_name = project_name
    property.seller = seller
    property.final_price = final_price
    property.property_type = PropertyTypes.PG
    property.address = property_address
    property.seller_contact = seller_contact
    property.map = property_map
    property.about_property = about_property
    property.updated_date = datetime.now()
    property.save()

    pg = PG.objects.get(property=property)

    pg.property = property
    pg.sharing_types = sharing_types
    pg.sharing_for = sharing_for
    pg.attached_washroom = attached_washroom
    pg.food_facility = food_facility
    pg.parking_facility = parking_facility
    pg.other_facilities = other_facilities
    pg.ready_to_move_in = ready_to_move_in
    pg.coliving_common_areas = coliving_common_areas
    pg.non_veg_available = non_veg_available
    pg.visitor_allowed = visitor_allowed
    pg.opposite_sex_visitor_allowed = opposite_sex_visitor_allowed
    pg.drinking_allowed = drinking_allowed
    pg.smoking_allowed = smoking_allowed
    pg.any_time_allowed = any_time_allowed
    pg.last_time_entry = last_time_entry
    pg.furnishing_detail = furnishing_detail
    pg.food_offerings = food_offerings
    pg.save()

    if image_details:
        add_property_images(
            property=property, property_images=property_images, image_details=image_details
        )

    return send_pass_http_response({"property_id": property.id})
