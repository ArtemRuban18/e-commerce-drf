from .services import CartService, WishlistService
from .serializers import (
    CartResponceSerializer,
    CartAddSerializer,
    CartUpdateSerializer,
    CartDeteteSerializer,
    WishlistResponceSerializer,
    WishlistAddSerializer,
    WishlistDeteteSerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .selectors import get_cart_products, get_wishlist_products
from .services import ShoppingService


class CartAPIView(APIView):
    def get_cart(self, request: Request) -> Response:
        shopping = ShoppingService(
            request.session,
            "cart"
        )
        return CartService(shopping)

    def get(self, request):
        cart  = self.get_cart(request)

        data = get_cart_products(cart.get_items())

        serializer = CartResponceSerializer(data)

        return Response(serializer.data)


    def post(self, request: Request) -> Response:
        cart  = self.get_cart(request)
        serializer = CartAddSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            cart.add(
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"]
            )

        return Response({
            "message":"Product add to cart"
        })
    
    def patch(self, request: Request) -> Response:
        cart  = self.get_cart(request)
        serializer = CartUpdateSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            cart.update(
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"]
            )

        return Response({
            "message":"Update quantity product in cart"
        })

    def delete(self, request: Request) -> Response:
        cart  = self.get_cart(request)
        serializer = CartDeteteSerializer(data = request.data)
        
        if serializer.is_valid(raise_exception=True):
            cart.remove(product_id = serializer.validated_data['product_id'])
        
        return Response({"message":"Product deleted from cart"})


class WishlistAPIView(APIView):
    def get_wishlist(self, request: Request) -> Response:
        shopping = ShoppingService(
            request.session,
            "wishlist"
        )
        return WishlistService(shopping)


    def get(self, request: Request) -> Response:
        wishlist = self.get_wishlist(request)

        data = get_wishlist_products(wishlist.get_items())

        serializer = WishlistResponceSerializer(data)

        return Response(serializer.data)


    def post(self, request: Request) -> Response:
        wishlist = self.get_wishlist(request)
        serializer = WishlistAddSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            wishlist.add(product_id = serializer.validated_data['product_id'])
        
        return Response({"message": "Product added to wishlist"})

    def delete(self, request: Request) -> Response:
        wishlist = self.get_wishlist(request)
        serializer = WishlistDeteteSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            wishlist.remove(product_id = serializer.validated_data['product_id'])

        return Response({"message": "Product deleted from wishlist"})