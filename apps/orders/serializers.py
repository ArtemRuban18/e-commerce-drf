from .models import Order, OrderItem
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = 'product.name', read_only = True)
    total_price_product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "product_name",
            "price",
            "quantity",
            "total_price_product",
        ]

    def get_total_price_product(self, obj):
        return obj.get_cost()
    
class OrderCreateSerializer(serializers.ModelSerializer):
    phone = serializers.RegexField(
        regex=r'^\+?[1-9]\d{7,14}$',
        error_messages={
            "invalid": "Enter a valid phone number"
        }
    )
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "address",
            "postal_code",
            "city",
            "payment_method",
        ]

class OrderResponseSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True, read_only = True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
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
            "items",
            "total_price"
        ]
    
    def get_total_price(self, obj):
        return obj.total_price()