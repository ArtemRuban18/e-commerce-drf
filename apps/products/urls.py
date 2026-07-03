from .views import (ProductListView,
                        ProductDetailView,
                        CategoryListView,
                        CategoryDetailView,
                        PhotoProductListView,
                        PhotoProductDetailView,)
from django.urls import path

urlpatterns = [
    path('products/', ProductListView.as_view(), name = 'product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('categories/', CategoryListView.as_view(), name = 'category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name = 'category-detail'),
    path('photo-products/', PhotoProductListView.as_view(), name = 'photo-product-list'),
    path('photo-products/<int:id>/', PhotoProductDetailView.as_view(), name = 'photo-product-detail'),
]