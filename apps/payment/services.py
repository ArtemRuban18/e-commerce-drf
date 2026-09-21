import stripe
from django.conf import settings
from .models import Payment
from typing import Tuple

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    
    @staticmethod
    def create_checkout_session(order) -> Tuple:
        total_price = order.total_price()
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "sek",

                        "unit_amount": int(
                            total_price * 100
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
            stripe_payment_id=session.id,
            amount=total_price,
            email=order.email,
            status=Payment.Status.PENDING,
        )

        return session, payment