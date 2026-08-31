from rest_framework import serializers


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value = 1, default = 1)

class CartUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value = 1)

class CartDeleteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

class CartResponseSerializer(serializers.Serializer):
    items = CartItemSerializer(many = True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = serializers.IntegerField()

class WishlistAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class WishlistDeleteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class WishlistItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class WishlistResponseSerializer(serializers.Serializer):
    items = WishlistItemSerializer(many = True)
    total_quantity = serializers.IntegerField()