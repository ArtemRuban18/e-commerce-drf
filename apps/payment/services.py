import stripe
from django.conf import settings
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    @staticmethod
    def create_checkout_session(order):
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

            success_url=("http://localhost:3000/payment/success"),

            cancel_url=( "http://localhost:3000/payment/cancel"),)

        payment = Payment.objects.create(
            stripe_payment_id=session.id,
            order=order,
            amount=order.total_price,
            email=order.email,
        )

        return session, payment