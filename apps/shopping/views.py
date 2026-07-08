from .services import CartService
from .serializers import CartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class CartAPIView(APIView):
    def get(self, request):
        cart = CartService(request)
        items = cart.get_items()
        return Response({
            "cart":items
        })


    def post(self, request):
        cart = CartService(request)
        serializer = CartSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            cart.add(
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"]
            )
        return Response({
            "message":"Product add to cart"
        })