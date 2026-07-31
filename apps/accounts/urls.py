from django.urls import path
from .views import SignUpAPIView, LoginAPiView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='sign-up'),
    path('login/', LoginAPiView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]