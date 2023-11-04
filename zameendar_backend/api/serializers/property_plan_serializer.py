from zameendar_backend.api.models import Order, PropertyModel, PropertyPlan


def property_plan_serializer(property_model: PropertyModel):
    property_plan = PropertyPlan.objects.filter(
        property_model=property_model, is_active=True
    ).first()

    serialized_data = None
    if property_plan:
        is_order_paid = Order.objects.filter(property_plan=property_plan, isPaid=True).exists()
        price = 0
        if property_plan.is_offer_taken:
            price = property_plan.plan.offer_price
        if is_order_paid:
            serialized_data = {
                "property_plan_id": property_plan.id,
                "plan_id": property_plan.plan.id,
                "plan_start_on": property_plan.plan_start_on,
                "plan_expire_on": property_plan.plan_expire_on,
                "plan_name": property_plan.plan.title,
                "plan_type": property_plan.plan.plan_type,
                "base_price": price,
            }
    return serialized_data
