import stripe
from django.conf import settings
from .models import Payment
from typing import Tuple

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    """Сервіс для обробки платежів через Stripe."""
    
    @staticmethod
    def create_checkout_session(order) -> Tuple:
        """
        Створити сесію оплати Stripe для замовлення.
        
        Args:
            order: Об'єкт замовлення
            
        Returns:
            Кортеж (session, payment) - сесія Stripe та запис платежу
        """
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "sek",

                        "unit_amount": int(
                            order.total_price * 100
                        ),

                        "product_data": {
                            "name": f"Order #{order.id}",
                        },
                    },

                    "quantity": 1,
                }
            ],

            mode="payment",

            metadata={
                "order_id": str(order.id),
            },

            customer_email=order.email,

            success_url=settings.STRIPE_SUCCESS_URL,

            cancel_url=settings.STRIPE_CANCEL_URL,)

        payment = Payment.objects.create(
            order=order,
            amount=order.total_price,
            email=order.email,
            status=Payment.Status.PENDING,
        )

        return session, payment