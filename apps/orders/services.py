from apps.products.models import Product
from .models import Order, OrderItem
from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.shopping.selectors import get_cart_products

class OrderService:
    @staticmethod
    def create_order(user, cart, data: dict[str, int]) -> Order:
        cart_items = cart.get_items()

        if not cart_items:
            raise ValidationError("Cart is empty")

        with transaction.atomic():
            products = Product.objects.select_for_update().filter(id__in=cart_items.keys())

            order = Order.objects.create(
                user = user,
                **data
            )

            #items list to add to the order
            order_items = []
            for product in products:
                quantity = cart_items[str(product.id)]

                if product.quantity < quantity:
                    raise ValidationError(f"Not enough {product.name}")

                order_items.append(
                    OrderItem(
                        order = order,
                        product = product,
                        price = product.price,
                        quantity = quantity
                    )
                )

                product.quantity -= quantity
                product.save()

            OrderItem.objects.bulk_create(order_items)
            cart.clear()

            return order

    @staticmethod
    @transaction.atomic
    def cancel_order(order: Order) -> Order:
        if order.status in [
            Order.Status.CANCELED,
            Order.Status.COMPLETED
        ]:
            raise ValidationError("Order cannot be canceled")

        for item in order.items.all():
            product = item.product

            product.quantity += item.quantity

            product.save()

        order.status = Order.Status.CANCELED
        order.save()

        return order        

