from rest_framework import generics
from .models import Category, Product, PhotoProduct
from .serializers import CategorySerializer, ProductSerializer, PhotoProductSerializer
from .services import ProductService
from config.pagination import StandartSetPagination
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from .filters import ProductFilter
from django_filters import rest_framework as filters

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

@method_decorator(cache_page(60 * 10), name='dispatch')
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class  = ProductSerializer
    pagination_class = StandartSetPagination
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter 

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = ProductService.get_products_by_category(category)
        return queryset
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class PhotoProductListView(generics.ListCreateAPIView):
    queryset = PhotoProduct.objects.all()
    serializer_class = PhotoProductSerializer
    permission_classes = [AllowAny]

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
    