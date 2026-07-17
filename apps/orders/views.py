from .serializers import OrderCreateSerializer, OrderResponseSerializer
from .services import OrderService
from apps.shopping.services import CartService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .selectors import get_user_order, get_user_orders

class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        order = get_user_order(
            user=request.user,
            order_id=id
        )

        if not order:
            return Response(
                {
                    "error": "Order not found"
                }
            )
        
        serializer = OrderResponseSerializer(order)
        return Response(serializer.data)

class OrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = get_user_orders(user = request.user)

        serializer = OrderResponseSerializer(orders, many = True)

        return Response(serializer.data)

    def post(self, request):

        serializer = OrderCreateSerializer(
            data = request.data
        )

        serializer.is_valid(raise_exception=True)
        cart = CartService(request)

        order = OrderService.create_order(
            user = request.user,
            cart = cart,
            data = serializer.validated_data
        )

        response = OrderResponseSerializer(order)
        return Response(response.data, status=status.HTTP_201_CREATED)



class OrderCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        order = get_user_order(
            user = request.user,
            order_id = id
        )

        if not order:
            return Response(
                {
                    "error": "Order not found"
                }
            )

        OrderService.cancel_order(order)

        serializer = OrderResponseSerializer(order)

        return Response(serializer.data)