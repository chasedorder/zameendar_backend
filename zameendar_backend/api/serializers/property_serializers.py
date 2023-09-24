from zameendar_backend.api.meta_models import PropertyTypes
from zameendar_backend.api.models import (
    PG,
    PROPERTY_MODEL_MAP,
    Building,
    Commercial,
    ContactDetails,
    Flat,
    GroupAppartment,
    GroupPlot,
    GroupVilla,
    OpenPlot,
    Property,
    PropertyAddress,
    PropertyMap,
    Rent,
    Seller,
    Villa,
)


def seller_serializer(seller: Seller):
    first_name = seller.user.first_name
    last_name = seller.user.last_name
    email = seller.user.email

    serialized_data = {"first_name": first_name, "last_name": last_name, "email": email}
    return serialized_data


def map_serializer(map_: PropertyMap):
    if not map_:
        return None
    location = map_.location

    serializerd_data = {"location": location}
    return serializerd_data


def seller_contact_serializer(seller_contact: ContactDetails):
    if not seller_contact:
        return None
    phone_number_1 = seller_contact.phone_number_1
    phone_number_2 = seller_contact.phone_number_2
    email = seller_contact.email

    serialized_data = {
        "phone_number_1": phone_number_1,
        "phone_number_2": phone_number_2,
        "email": email,
    }
    return serialized_data


def property_address_serializer(address: PropertyAddress):
    if not address:
        return None
    street_address = address.street_address
    city = address.city
    state = address.state
    postal_code = address.postal_code
    area = address.area

    serialized_data = {
        "street_address": street_address,
        "city": city,
        "state": state,
        "postal_code": postal_code,
        "area": area,
    }
    return serialized_data


def group_appartment_serializer(group_appartment: GroupAppartment):
    price_per_sqft = group_appartment.price_per_sqft
    bhk_details = group_appartment.bhk_details
    number_of_floors = group_appartment.number_of_floors
    ready_to_occupy = group_appartment.ready_to_occupy
    possession_date = group_appartment.possession_date
    number_of_car_parking = group_appartment.number_of_car_parking
    number_of_bike_parking = group_appartment.number_of_bike_parking
    project_area = group_appartment.project_area
    project_size = group_appartment.project_size
    rera_id = group_appartment.rera_id
    sale_type = group_appartment.sale_type
    property_age = group_appartment.property_age
    number_of_bedrooms = group_appartment.number_of_bedrooms
    number_of_bathrooms = group_appartment.number_of_bathrooms
    rera_id = group_appartment.rera_id
    facing = group_appartment.facing
    furnishing_detail = group_appartment.furnishing_detail
    project_size = group_appartment.project_size
    sale_type = group_appartment.sale_type
    serialized_data = {
        "price_per_sqft": price_per_sqft,
        "bhk_details": bhk_details,
        "number_of_floors": number_of_floors,
        "ready_to_occupy": ready_to_occupy,
        "possession_date": possession_date,
        "number_of_car_parking": number_of_car_parking,
        "number_of_bike_parking": number_of_bike_parking,
        "project_area": project_area,
        "project_size": project_size,
        "rera_id": rera_id,
        "sale_type": sale_type,
        "property_age": property_age,
        "number_of_bedrooms": number_of_bedrooms,
        "number_of_bathrooms": number_of_bathrooms,
        "rera_id": rera_id,
        "facing": facing,
        "furnishing_detail": furnishing_detail,
        "project_size": project_size,
        "sale_type": sale_type,
    }

    return serialized_data


def group_villa_serializer(group_villa: GroupVilla):
    price_per_sqft = group_villa.price_per_sqft
    bhk_details = group_villa.bhk_details
    number_of_floors = group_villa.number_of_floors
    land_area_sizes = group_villa.land_area_sizes
    ready_to_occupy = group_villa.ready_to_occupy
    possession_date = group_villa.possession_date
    number_of_car_parking = group_villa.number_of_car_parking
    number_of_bike_parking = group_villa.number_of_bike_parking
    land_width = group_villa.land_width
    land_length = group_villa.land_length
    total_project_area = group_villa.total_project_area
    rera_id = group_villa.rera_id
    facing = group_villa.facing
    furnishing_detail = group_villa.furnishing_detail
    project_size = group_villa.project_size
    sale_type = group_villa.sale_type

    serialized_data = {
        "price_per_sqft": price_per_sqft,
        "bhk_details": bhk_details,
        "number_of_floors": number_of_floors,
        "land_area_sizes": land_area_sizes,
        "ready_to_occupy": ready_to_occupy,
        "possession_date": possession_date,
        "number_of_car_parking": number_of_car_parking,
        "number_of_bike_parking": number_of_bike_parking,
        "land_width": land_width,
        "land_length": land_length,
        "total_project_area": total_project_area,
        "rera_id": rera_id,
        "facing": facing,
        "furnishing_detail": furnishing_detail,
        "project_size": project_size,
        "sale_type": sale_type,
    }

    return serialized_data


def group_plot_serializer(group_plot: GroupPlot):
    price_per_sqyd = group_plot.price_per_sqyd
    plot_sizes = group_plot.plot_sizes
    total_project_area = group_plot.total_project_area
    rera_id = group_plot.rera_id
    facing = group_plot.facing
    serialized_data = {
        "price_per_sqyd": price_per_sqyd,
        "plot_sizes": plot_sizes,
        "total_project_area": total_project_area,
        "rera_id": rera_id,
        "facing": facing,
    }

    return serialized_data


def flat_serializer(flat: Flat):
    facing = flat.facing
    carpet_area = flat.carpet_area
    bedroom_available = flat.bedroom_available
    number_of_washrooms = flat.number_of_washrooms
    floor_number = flat.floor_number
    number_of_car_parking = flat.number_of_car_parking
    number_of_bike_parking = flat.number_of_bike_parking
    furnishing_detail = flat.furnishing_detail
    ready_to_occupy = flat.ready_to_occupy
    available_from = flat.available_from
    price_per_square_feet = flat.price_per_square_feet
    sale_type = flat.sale_type

    serialized_data = {
        "facing": facing,
        "carpet_area": carpet_area,
        "bedroom_available": bedroom_available,
        "number_of_washrooms": number_of_washrooms,
        "floor_number": floor_number,
        "number_of_car_parking": number_of_car_parking,
        "number_of_bike_parking": number_of_bike_parking,
        "furnishing_detail": furnishing_detail,
        "ready_to_occupy": ready_to_occupy,
        "available_from": available_from,
        "price_per_square_feet": price_per_square_feet,
        "sale_type": sale_type,
    }

    return serialized_data


def villa_serializer(villa: Villa):
    facing = villa.facing
    land_size = villa.land_size
    land_width = villa.land_width
    land_length = villa.land_length
    carpet_area = villa.carpet_area
    bedroom_available = villa.bedroom_available
    number_of_washrooms = villa.number_of_washrooms
    number_of_floors = villa.number_of_floors
    number_of_car_parking = villa.number_of_car_parking
    number_of_bike_parking = villa.number_of_bike_parking
    furnishing_detail = villa.furnishing_detail
    ready_to_occupy = villa.ready_to_occupy
    available_from = villa.available_from
    price_per_square_feet = villa.price_per_square_feet
    floors = villa.floors
    sale_type = villa.sale_type

    serialized_data = {
        "facing": facing,
        "land_size": land_size,
        "land_width": land_width,
        "land_length": land_length,
        "carpet_area": carpet_area,
        "bedroom_available": bedroom_available,
        "number_of_washrooms": number_of_washrooms,
        "number_of_floors": number_of_floors,
        "number_of_car_parking": number_of_car_parking,
        "number_of_bike_parking": number_of_bike_parking,
        "furnishing_detail": furnishing_detail,
        "ready_to_occupy": ready_to_occupy,
        "available_from": available_from,
        "price_per_square_feet": price_per_square_feet,
        "floors": floors,
        "sale_type": sale_type,
    }

    return serialized_data


def building_serializer(building: Building):
    facing = building.facing
    land_size = building.land_size
    land_width = building.land_width
    land_length = building.land_length
    carpet_area = building.carpet_area
    number_of_floors = building.number_of_floors
    number_of_car_parking = building.number_of_car_parking
    number_of_bike_parking = building.number_of_bike_parking
    ready_to_occupy = building.ready_to_occupy
    available_from = building.available_from
    sale_type = building.sale_type
    furnishing_detail = building.furnishing_detail
    bedroom_available = building.bedroom_available

    serialized_data = {
        "facing": facing,
        "land_size": land_size,
        "land_width": land_width,
        "land_length": land_length,
        "carpet_area": carpet_area,
        "number_of_floors": number_of_floors,
        "number_of_car_parking": number_of_car_parking,
        "number_of_bike_parking": number_of_bike_parking,
        "ready_to_occupy": ready_to_occupy,
        "available_from": available_from,
        "sale_type": sale_type,
        "furnishing_detail": furnishing_detail,
        "bedroom_available": bedroom_available,
    }

    return serialized_data


def open_plot_serializer(open_plot: OpenPlot):
    facing = open_plot.facing
    land_size = open_plot.land_size
    land_width = open_plot.land_width
    land_length = open_plot.land_length
    is_fencing = open_plot.is_fencing
    price_per_square_yard = open_plot.price_per_square_yard
    serialized_data = {
        "facing": facing,
        "land_size": land_size,
        "land_width": land_width,
        "land_length": land_length,
        "is_fencing": is_fencing,
        "price_per_square_yard": price_per_square_yard,
    }

    return serialized_data


def rent_serializer(rent: Rent):
    facing = rent.facing
    floor_number = rent.floor_number
    number_of_car_parking = rent.number_of_car_parking
    number_of_bike_parking = rent.number_of_bike_parking
    furnishing_detail = rent.furnishing_detail
    rent_per_month = rent.rent_per_month
    advance_amount = rent.advance_amount
    ready_to_move_in = rent.ready_to_move_in
    carpet_area = rent.carpet_area
    bedroom_available = rent.bedroom_available

    serialized_data = {
        "facing": facing,
        "floor_number": floor_number,
        "number_of_car_parking": number_of_car_parking,
        "number_of_bike_parking": number_of_bike_parking,
        "furnishing_detail": furnishing_detail,
        "rent_per_month": rent_per_month,
        "advance_amount": advance_amount,
        "ready_to_move_in": ready_to_move_in,
        "carpet_area": carpet_area,
        "bedroom_available": bedroom_available,
    }

    return serialized_data


def pg_serializer(pg: PG):
    sharing_type = pg.sharing_type
    sharing_for = pg.sharing_for
    attached_washroom = pg.attached_washroom
    food_facility = pg.food_facility
    parking_facility = pg.parking_facility
    price_per_month = pg.price_per_month
    advance_amount = pg.advance_amount
    other_facilities = pg.other_facilities
    ready_to_move_in = pg.ready_to_move_in
    coliving_common_area = pg.coliving_common_area
    non_veg_available = pg.non_veg_available
    visitor_allowed = pg.visitor_allowed
    opposite_sex_visitor_allowed = pg.opposite_sex_visitor_allowed
    drinking_allowed = pg.drinking_allowed
    smoking_allowed = pg.smoking_allowed
    any_time_allowed = pg.any_time_allowed
    last_time_entry = pg.last_time_entry
    furnishing_detail = pg.furnishing_detail
    food_offerings = pg.food_offerings

    serialized_data = {
        "sharing_type": sharing_type,
        "sharing_for": sharing_for,
        "attached_washroom": attached_washroom,
        "food_facility": food_facility,
        "parking_facility": parking_facility,
        "price_per_month": price_per_month,
        "advance_amount": advance_amount,
        "other_facilities": other_facilities,
        "ready_to_move_in": ready_to_move_in,
        "coliving_common_area": coliving_common_area,
        "non_veg_available": non_veg_available,
        "visitor_allowed": visitor_allowed,
        "opposite_sex_visitor_allowed": opposite_sex_visitor_allowed,
        "drinking_allowed": drinking_allowed,
        "smoking_allowed": smoking_allowed,
        "any_time_allowed": any_time_allowed,
        "last_time_entry": last_time_entry,
        "furnishing_detail": furnishing_detail,
        "food_offerings": food_offerings,
    }

    return serialized_data


def commercial_serializer(commercial: Commercial):
    commerical_category = commercial.commerical_category
    price_per_square_feet = commercial.price_per_square_feet
    builtup_area = commercial.builtup_area
    price_per_square_yard = commercial.price_per_square_yard
    passenger_lifts = commercial.passenger_lifts
    service_lifts = commercial.service_lifts
    parking_available = commercial.parking_available
    min_contract_period = commercial.min_contract_period
    negotialble = commercial.negotialble
    tax_gov_charges_included = commercial.tax_gov_charges_included
    dg_ups_charges_included = commercial.dg_ups_charges_included
    water_charges_included = commercial.water_charges_included
    floor_number = commercial.floor_number
    possesstion_date = commercial.possesstion_date
    electricity_bill_included = commercial.electricity_bill_included
    safety_deposit = commercial.safety_deposit
    rent_per_month = commercial.rent_per_month

    serialized_data = {
        "commerical_category": commerical_category,
        "price_per_square_feet": price_per_square_feet,
        "builtup_area": builtup_area,
        "price_per_square_yard": price_per_square_yard,
        "passenger_lifts": passenger_lifts,
        "service_lifts": service_lifts,
        "parking_available": parking_available,
        "min_contract_period": min_contract_period,
        "negotialble": negotialble,
        "tax_gov_charges_included": tax_gov_charges_included,
        "dg_ups_charges_included": dg_ups_charges_included,
        "water_charges_included": water_charges_included,
        "floor_number": floor_number,
        "possesstion_date": possesstion_date,
        "electricity_bill_included": electricity_bill_included,
        "safety_deposit": safety_deposit,
        "rent_per_month": rent_per_month,
    }

    return serialized_data


PROPERTY_SERIALIZER_MAP = {
    PropertyTypes.GroupAppart: group_appartment_serializer,
    PropertyTypes.GroupVilla: group_villa_serializer,
    PropertyTypes.GroupPlot: group_plot_serializer,
    PropertyTypes.Flat: flat_serializer,
    PropertyTypes.Villa: villa_serializer,
    PropertyTypes.Building: building_serializer,
    PropertyTypes.OpenPlot: open_plot_serializer,
    PropertyTypes.Rent: rent_serializer,
    PropertyTypes.PG: pg_serializer,
    PropertyTypes.Commercial: commercial_serializer,
}


def property_serializer(property: Property):
    property_id = property.id
    project_name = property.project_name
    property_type = property.property_type
    address = property_address_serializer(property.address)
    map_details = map_serializer(property.map)
    seller_contact = seller_contact_serializer(property.seller_contact)
    start_price = property.start_price
    end_price = property.end_price
    final_price = property.final_price
    amenities = property.amenities
    is_verified = property.is_verified
    about_property = property.about_property

    serialized_data = {
        "property_id": property_id,
        "project_name": project_name,
        "property_type": property_type,
        "address": address,
        "map_details": map_details,
        "seller_contact": seller_contact,
        "start_price": start_price,
        "end_price": end_price,
        "final_price": final_price,
        "amenities": amenities,
        "is_verified": is_verified,
        "about_property": about_property,
    }

    property_type_details = PROPERTY_SERIALIZER_MAP.get(property_type)

    serialized_data.update(
        property_type_details(PROPERTY_MODEL_MAP.get(property_type).objects.get(property=property))
    )

    return serialized_data
