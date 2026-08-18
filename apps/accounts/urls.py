from django.urls import path
from .views import RegisterAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('auth//login/token/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/refres/', TokenRefreshView.as_view(), name='refresh'),
    path('auth/register/', RegisterAPIView.as_view(), name = 'register'),
]