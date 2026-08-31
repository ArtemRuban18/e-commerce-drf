from django.db import models
from apps.orders.models import Order

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        PAID = 'paid'
        CANCEL = 'cancel'


    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    status = models.CharField(max_length=50, choices=Status.choices, default = Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return f"Payment {self.id} - Order #{self.order.id} - {self.status}"