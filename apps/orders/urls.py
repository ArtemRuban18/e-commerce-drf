from django.urls import path
from .views import (
    OrderListCreateAPIView,
    OrderCancelAPIView,
    OrderDetailAPIView,
)

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name = 'orders'),
    path('orders/<int:id>', OrderDetailAPIView.as_view(), name = 'detail-order'),
    path('orders/<int:id>/cancel/', OrderCancelAPIView.as_view(), name='cancel-order'),
]