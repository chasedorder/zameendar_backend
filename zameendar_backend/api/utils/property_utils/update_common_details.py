from zameendar_backend.api.models import ContactDetails, PropertyAddress, PropertyMap


def update_common_details(
    property_model, maps_details=None, address_details=None, contact_details=None
):
    property_map = None
    property_address = None
    seller_contact = None

    if maps_details:
        property_map = property_model.map
        if property_map:
            property_map.location = maps_details.get("location")
            property_map.save()
        else:
            property_map = PropertyMap.objects.create(
                location=maps_details.get("location")
            )
    if address_details:
        property_address = property_model.address
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
        seller_contact = property_model.seller_contact
        if seller_contact:
            seller_contact.phone_number_1 = contact_details.get("phone_number_1")
            seller_contact.phone_number_2 = contact_details.get("phone_number_2")
            seller_contact.email = contact_details.get("email")
            seller_contact.name = contact_details.get("name")
            seller_contact.save()
        else:
            seller_contact = ContactDetails.objects.create(
                phone_number_1=contact_details.get("phone_number_1"),
                phone_number_2=contact_details.get("phone_number_2"),
                email=contact_details.get("email"),
                name=contact_details.get("name"),
            )

    return (property_map, property_address, seller_contact)
