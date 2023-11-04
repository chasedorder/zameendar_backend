from zameendar_backend.api.models import ContactDetails, PropertyAddress, PropertyMap


def update_common_details(property, maps_details=None, address_details=None, contact_details=None):
    property_map = None
    property_address = None
    seller_contact = None

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

    return (property_map, property_address, seller_contact)
