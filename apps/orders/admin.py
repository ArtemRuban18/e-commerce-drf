from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = True

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "address",
        "postal_code",
        "city",
        "status",
        "payment_method",
        "total_price"
    ]
    search_fields = ["phone", "email"]
    readonly_fields = ["email","total_price"]
    ordering = ["-created"]
    inlines = [OrderItemInline]