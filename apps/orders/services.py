from apps.products.models import Product
from .models import Order, OrderItem
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .tasks import order_created
from typing import Dict
from django.contrib.auth.models import User


class OrderService:
    """Сервіс для управління замовленнями."""
    
    @staticmethod
    @transaction.atomic
    def create_order(user: User, cart, data: Dict[str, str]) -> Order:
        """
        Створити замовлення з товарів кошика.
        
        Args:
            user: Користувач який замовляє
            cart: Об'єкт кошика
            data: Дані замовлення (ім'я, адреса, тощо)
            
        Returns:
            Створене замовлення
            
        Raises:
            ValidationError: Якщо кошик пустий або недостатньо товарів
        """
        cart_items = cart.get_items()

        if not cart_items:
            raise ValidationError("Cart is empty")
        
        products = Product.objects.select_for_update().filter(id__in=cart_items.keys())

        order = Order.objects.create(
            user = user,
            **data
        )

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

        transaction.on_commit(
            lambda: order_created.apply_async(
                    args=[order.id],
                    queue="emails",
    )
)
        
        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(order: Order) -> Order:
        """
        Скасувати замовлення та повернути товари на склад.
        
        Args:
            order: Замовлення для скасування
            
        Returns:
            Скасоване замовлення
            
        Raises:
            ValidationError: Якщо замовлення не в статусі PENDING
        """
        if order.status != Order.Status.PENDING:
            raise ValidationError("Only pending orders can be canceled")

        for item in order.items.all():
            product = item.product

            product.quantity += item.quantity

            product.save()

        order.status = Order.Status.CANCELLED
        order.save()

        return order        

