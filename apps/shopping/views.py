from .services import CartService
from .serializers import (
    CartResponceSerializer,
    CartAddSerializer,
    CartUpdateSerializer,
    CartDeteteSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.products.models import Product
class CartAPIView(APIView):
    def get(self, request):
        cart  = CartService(request)

        items = []
        products = Product.objects.filter(id__in = cart.items.keys())
        for product in products:
            quantity = cart.items[str(product.id)]

            items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "total_price": product.price * quantity
            })
        
        data = {
            "items": items,
            "total_price": cart.get_total_price(),
            "total_quantity": len(cart)
        }

        serializer = CartResponceSerializer(instance=data)
        return Response(serializer.data)


    def post(self, request):
        cart = CartService(request)
        serializer = CartAddSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            cart.add(
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"]
            )
        return Response({
            "message":"Product add to cart"
        })
    
    def patch(self, request):
        cart = CartService(request)
        serializer = CartUpdateSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            cart.update(
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"]
            )
        return Response({
            "message":"Update quantity product in cart"
        })

    def delete(self, request):
        cart = CartService(request)
        serializer = CartDeteteSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            cart.remove(product_id = serializer.validated_data['product_id'])
        
        return Response({"message":"Product deleted from cart"})