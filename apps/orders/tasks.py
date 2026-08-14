from celery import shared_task
from django.core.mail import send_mail
from apps.orders.models import Order
from django.core.exceptions import ObjectDoesNotExist
from config.settings.base import EMAIL_HOST_USER

@shared_task(
        name = "send_email_order",
        autoretry_for = (ConnectionError,),
        max_retries = 3,
        retry_backoff = True
)
def order_created(order_id: int):

    try:
        order = Order.objects.get(id = order_id)
    except ObjectDoesNotExist:
        return None

    subject = f"Order successfully accepted!"
    message = (
        f'Dear {order.first_name}, \n\n'
        f'You have successfully placed an order.'
        f'Your order ID is {order.id}'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[order.email]
    )