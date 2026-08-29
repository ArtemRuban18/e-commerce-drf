import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.orders.models import Order
from .serializers import PaymentSerializer
from .services import PaymentService
from django.conf import settings
from django.db import transaction
from .models import Payment


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentSerializer( data=request.data)

        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data["order_id"]
        try:
            order = Order.objects.get(
                id=order_id,
                user=request.user,
            )
        except Order.DoesNotExist:
            return Response(
                {
                    "detail": "Order not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.status != Order.Status.PENDING:
            return Response(
                {
                    "detail": "Order cannot be paid."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            session, payment = (
                PaymentService.create_checkout_session(
                    order
                )
            )
        except stripe.error.StripeError:
            return Response(
                {
                    "detail": "Stripe payment error."
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )
        return Response(
            {
                "checkout_url": session.url,
                "session_id": session.id,
            },
            status=status.HTTP_201_CREATED,
        )

class StripeWebhookView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        payload = request.body

        sig_header = request.META.get(
            "HTTP_STRIPE_SIGNATURE"
        )

        try:

            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET,
            )

        except ValueError:

            return Response(
                {"detail": "Invalid payload"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except stripe.error.SignatureVerificationError:

            return Response(
                {"detail": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event["type"] == "checkout.session.completed":

            session = event["data"]["object"]

            try:

                payment = (
                    Payment.objects
                    .select_related("order")
                    .get(
                        stripe_payment_id=session["id"]
                    )
                )

            except Payment.DoesNotExist:

                return Response(
                    {"detail": "Payment not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            with transaction.atomic():

                if payment.status == Payment.Status.PAID:

                    return Response(
                        {"status": "already processed"},
                        status=status.HTTP_200_OK,
                    )
                payment.status = Payment.Status.PAID
                payment.save(
                    update_fields=["status"]
                )
                order = payment.order
                order.status = order.Status.PAID

                order.save(
                    update_fields=["status"]
                )

        return Response(
            {"status": "success"},
            status=status.HTTP_200_OK,
        )