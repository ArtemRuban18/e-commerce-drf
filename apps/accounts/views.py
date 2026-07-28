from rest_framework.response import Response
from .serializers import SignUpSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class SignUpAPIView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            return Response({
                "message": "User created successfully",
                "username": user.username,
            },
            status=status.HTTP_201_CREATED

            )

        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

class LoginAPiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)

        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credential"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

