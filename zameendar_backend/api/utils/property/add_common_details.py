from zameendar_backend.api.models import ContactDetails, PropertyAddress, PropertyMap


def add_common_details(maps_details=None, address_details=None, contact_details=None):
    property_map = None
    property_address = None
    seller_contact = None

    if maps_details:
        property_map = PropertyMap.objects.create(location=maps_details.get("location"))

    if address_details:
        property_address = PropertyAddress.objects.create(
            street_address=address_details.get("street_address"),
            area=address_details.get("area"),
            city=address_details.get("city"),
            state=address_details.get("state"),
            postal_code=address_details.get("postal_code"),
        )

    if contact_details:
        seller_contact = ContactDetails.objects.create(
            phone_number_1=contact_details.get("phone_number_1"),
            phone_number_2=contact_details.get("phone_number_2"),
            email=contact_details.get("email"),
        )

    return (property_map, property_address, seller_contact)
