from django.urls import path
from .views import CreateCheckoutSessionView, StripeWebhookView


urlpatterns = [

    path("orders/pay/",CreateCheckoutSessionView.as_view(),name="create-checkout",),

    path("stripe/webhook/",StripeWebhookView.as_view(), name="stripe-webhook", ),
]