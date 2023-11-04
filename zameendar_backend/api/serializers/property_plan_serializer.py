from zameendar_backend.api.models import Order, Property, PropertyPlan


def property_plan_serializer(property: Property):
    property_plan = PropertyPlan.objects.filter(property=property, is_active=True).first()

    serialized_data = None
    if property_plan:
        is_order_paid = Order.objects.filter(property_plan=property_plan, isPaid=True).exists()
        if is_order_paid:
            serialized_data = {
                "property_plan_id": property_plan.id,
                "plan_id": property_plan.plan.id,
                "plan_start_on": property_plan.plan_start_on,
                "plan_expire_on": property_plan.plan_expire_on,
            }
    return serialized_data
