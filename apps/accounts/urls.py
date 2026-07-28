from django.urls import path
from .views import SignUpAPIView, LoginAPiView


urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='sign-up'),
    path('login/', LoginAPiView.as_view(), name='login'),
]