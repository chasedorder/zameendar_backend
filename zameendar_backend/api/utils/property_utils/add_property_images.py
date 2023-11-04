from zameendar_backend.api.models import PropertyImage


def add_property_images(property_model, property_images, image_details):
    property_images_obj_list = []
    for image, image_detail in zip(property_images, image_details):
        property_images_obj_list.append(
            PropertyImage(
                title=image_detail["title"],
                property_model=property_model,
                meta_data=image_detail["meta_data"],
                image=image,
            )
        )
    PropertyImage.objects.bulk_create(property_images_obj_list)
