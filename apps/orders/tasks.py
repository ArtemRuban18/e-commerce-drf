from celery import shared_task
from django.core.mail import send_mail
from apps.orders.models import Order
from config.settings.base import EMAIL_HOST_USER

@shared_task
def order_created(order_id):

    order = Order.objects.get(id = order_id)

    subject = f"Order successfully accepted!"
    message = (
        f'Dear {order.first_name}, \n\n'
        f'You have successfully placed an order.'
        f'Your order ID is {order.id}'
    )

    mail_sent = send_mail(
        subject, message, EMAIL_HOST_USER, [order.email]
    )