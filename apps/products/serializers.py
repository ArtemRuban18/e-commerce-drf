from rest_framework import serializers
from .models import Category, Product, PhotoProduct

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all())
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'status', 'price', 'quantity']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value
    
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value
    
    def validate(self, data):
        if data['status'] == Product.Status.OUT_OF_STOCK and data['quantity'] > 0:
            raise serializers.ValidationError("Out of stock products cannot have a quantity greater than zero")
        return data

class PhotoProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source = 'product.name', read_only = True)
    class Meta:
        model = PhotoProduct
        fields = ['product', 'image', 'is_main']

    def validate_photo(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size should not exceed 2MB")
        
        allowed_formats = ['image/jpeg', 'image/png']
        if value.content_type not in allowed_formats:
            raise serializers.ValidationError("Unsupported image format. Only JPEG and PNG are allowed.")
        
        return value