from decimal import Decimal
from unittest.mock import Mock, patch

import stripe
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.orders.models import Order
from apps.payment.models import Payment
from apps.payment.services import PaymentService


class PaymentTestMixin:
	def create_order(self, user, status=Order.Status.PENDING):
		return Order.objects.create(
			user=user,
			first_name="Test",
			last_name="User",
			phone="+46123456789",
			email="test@example.com",
			address="Test address",
			postal_code="12345",
			city="Stockholm",
			status=status,
		)


class PaymentServiceTests(PaymentTestMixin, APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="payment-user",
			password="test-password",
		)
		self.order = self.create_order(self.user)

	@patch("apps.payment.services.stripe.checkout.Session.create")
	def test_create_checkout_session_creates_pending_payment(self, create_session):
		create_session.return_value = Mock(id="cs_test_123", url="https://checkout.test")

		session, payment = PaymentService.create_checkout_session(self.order)

		create_session.assert_called_once_with(
			payment_method_types=["card"],
			line_items=[{
				"price_data": {
					"currency": "sek",
					"unit_amount": 0,
					"product_data": {"name": f"Order #{self.order.id}"},
				},
				"quantity": 1,
			}],
			mode="payment",
			metadata={"order_id": str(self.order.id)},
			customer_email=self.order.email,
			success_url="http://localhost:3000/payment/success",
			cancel_url="http://localhost:3000/payment/cancel",
		)
		self.assertEqual(session.id, "cs_test_123")
		self.assertEqual(payment.stripe_payment_id, "cs_test_123")
		self.assertEqual(payment.amount, Decimal("0"))
		self.assertEqual(payment.status, Payment.Status.PENDING)


class CreateCheckoutSessionViewTests(PaymentTestMixin, APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="checkout-user",
			password="test-password",
		)
		self.order = self.create_order(self.user)
		self.url = reverse("create-checkout")

	def test_requires_authentication(self):
		response = self.client.post(self.url, {"order_id": self.order.id})

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	@patch("apps.payment.views.PaymentService.create_checkout_session")
	def test_creates_checkout_session_for_users_pending_order(self, create_session):
		create_session.return_value = (Mock(id="cs_test_123", url="https://checkout.test"), Mock())
		self.client.force_authenticate(self.user)

		response = self.client.post(self.url, {"order_id": self.order.id})

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data, {
			"checkout_url": "https://checkout.test",
			"session_id": "cs_test_123",
		})
		create_session.assert_called_once_with(self.order)

	def test_does_not_allow_paying_another_users_order(self):
		other_user = User.objects.create_user(username="other-user")
		other_order = self.create_order(other_user)
		self.client.force_authenticate(self.user)

		response = self.client.post(self.url, {"order_id": other_order.id})

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_does_not_allow_paying_non_pending_order(self):
		self.order.status = Order.Status.PAID
		self.order.save(update_fields=["status"])
		self.client.force_authenticate(self.user)

		response = self.client.post(self.url, {"order_id": self.order.id})

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	@patch("apps.payment.views.PaymentService.create_checkout_session")
	def test_returns_bad_gateway_when_stripe_fails(self, create_session):
		create_session.side_effect = stripe.error.StripeError("Stripe is unavailable")
		self.client.force_authenticate(self.user)

		response = self.client.post(self.url, {"order_id": self.order.id})

		self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)


class StripeWebhookViewTests(PaymentTestMixin, APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="webhook-user")
		self.order = self.create_order(self.user)
		self.payment = Payment.objects.create(
			order=self.order,
			stripe_payment_id="cs_test_123",
			amount=Decimal("100.00"),
			email=self.order.email,
		)
		self.url = reverse("stripe-webhook")

	def post_webhook(self, payload=b"{}"): 
		return self.client.generic(
			"POST",
			self.url,
			payload,
			content_type="application/json",
		)

	@patch("apps.payment.views.stripe.Webhook.construct_event")
	def test_marks_payment_and_order_as_paid(self, construct_event):
		construct_event.return_value = {
			"type": "checkout.session.completed",
			"data": {"object": {"id": "cs_test_123"}},
		}

		response = self.client.post(
			self.url,
			data=b"{}",
			content_type="application/json",
			HTTP_STRIPE_SIGNATURE="valid-signature",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.payment.refresh_from_db()
		self.order.refresh_from_db()
		self.assertEqual(self.payment.status, Payment.Status.PAID)
		self.assertEqual(self.order.status, Order.Status.PAID)

	@patch("apps.payment.views.stripe.Webhook.construct_event")
	def test_is_idempotent_for_paid_payment(self, construct_event):
		self.payment.status = Payment.Status.PAID
		self.payment.save(update_fields=["status"])
		construct_event.return_value = {
			"type": "checkout.session.completed",
			"data": {"object": {"id": "cs_test_123"}},
		}

		response = self.post_webhook()

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, {"status": "already processed"})

	@patch("apps.payment.views.stripe.Webhook.construct_event")
	def test_returns_not_found_for_unknown_payment(self, construct_event):
		construct_event.return_value = {
			"type": "checkout.session.completed",
			"data": {"object": {"id": "unknown"}},
		}

		response = self.post_webhook()

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	@patch("apps.payment.views.stripe.Webhook.construct_event")
	def test_rejects_invalid_signature(self, construct_event):
		construct_event.side_effect = stripe.error.SignatureVerificationError(
			"Invalid signature", "signature"
		)

		response = self.post_webhook()

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	@patch("apps.payment.views.stripe.Webhook.construct_event")
	def test_rejects_invalid_payload(self, construct_event):
		construct_event.side_effect = ValueError("Invalid payload")

		response = self.post_webhook(payload=b"invalid")

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
