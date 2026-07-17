from django.db import models
from apps.products.models import Product
from django.contrib.auth.models import User
from django.db.models import Sum, F



class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new',  'NEW'
        PROCESSING = 'processing', 'PROCESSING'
        APPROVED = 'approved', 'APPROVED'
        SHIPPED = 'shipped', 'SHIPPED'
        DELIVERED = 'delivered', 'DELIVERED'
        COMPLETED = 'completed', 'COMPLETED'
        CANCELED = 'canceled', 'CANCELED'
    
    class PaymentMethod(models.TextChoices):
        ONLINE = 'online', 'ONLINE'
        COD = 'cod', 'COD'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=False)
    email = models.EmailField(blank=False)
    address = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20, blank = False)
    city = models.CharField(max_length=50, blank = False)
    status = models.CharField(max_length=20, choices = Status.choices, default = Status.NEW)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.ONLINE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def total_price(self):
        return self.items.aggregate(
            total = Sum(
                F("price") * F("quantity")
            )
        )["total"] or 0
    
    
    def __str__(self):
        return f'Order {self.id}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default = 1)

    def get_cost(self):
        return self.price * self.quantity
    
    def __str__(self):
        return str(self.id)