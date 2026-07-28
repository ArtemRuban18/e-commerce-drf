from rest_framework.response import Response
from .serializers import SignUpSerializer
from rest_framework.views import APIView
from rest_framework import status

class SignUpAPIView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data = request.data)

        if serializer.is_valid():
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
