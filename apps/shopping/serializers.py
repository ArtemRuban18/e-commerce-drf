from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value = 1, required = False)

class CartUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value = 1)

class CartDeteteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class CartResponceSerializer(serializers.Serializer):
    items = CartItemSerializer(many = True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = serializers.IntegerField()