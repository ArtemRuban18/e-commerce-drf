from django.shortcuts import render
from rest_framework import generics
from .models import Category, Product, PhotoProduct
from .serializers import CategorySerializer, ProductSerializer, PhotoProductSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class  = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug = category)
        return queryset
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class PhotoProductListView(generics.ListCreateAPIView):
    queryset = PhotoProduct.objects.all()
    serializer_class = PhotoProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product__id = product_id)
        
        return queryset

class PhotoProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhotoProduct.objects.all()
    serializer_class = PhotoProductSerializer
    lookup_field = 'id'
    