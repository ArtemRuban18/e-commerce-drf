from django.urls import path
from .views import CartAPIView, WishlistAPIView

urlpatterns = [
    path('cart/', CartAPIView.as_view(), name = 'cart'),
    path('wishlist/', WishlistAPIView.as_view(), name = 'wishlist'),
]