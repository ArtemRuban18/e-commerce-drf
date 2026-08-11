from .serializers import OrderCreateSerializer, OrderResponseSerializer
from .services import OrderService
from apps.shopping.services import ShoppingService, CartService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Order
from rest_framework.decorators import action

class OrderViewSet(ModelViewSet):
    serializer_class = OrderResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer

        return OrderResponseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        serializer.is_valid(raise_exception = True)

        cart = CartService(
            ShoppingService(
                session=request.session,
                key="cart"
            )
        )

        order = OrderService.create_order(
            user = request.user,
            cart = cart,
            data = serializer.validated_data
        )

        response_serializer = OrderResponseSerializer(order)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
            )

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk = None):
        order = self.get_object()

        order = OrderService.cancel_order(order = order)

        serializer = OrderResponseSerializer(order)

        return Response(serializer.data)
        