from .models import Order

def get_user_orders(user):
    return (Order.objects
            .filter(user=user)
            .prefetch_related("items__product")
            )

def get_user_order(user, order_id):
    return (Order.objects
            .filter(user = user, id = order_id)
            .prefetch_related("items__product")
            .first()
            )