from rest_framework.test import APITestCase
from apps.orders.models import Order, OrderItem
from apps.products.models import Product, Category
from apps.orders.services import OrderService
from django.contrib.auth.models import User
from apps.shopping.services import ShoppingService, CartService

class OrderServiceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password = 'testpassword')
        self.category = Category.objects.create(name = 'test')
        self.product = Product.objects.create(
            name = 'Test product',
            description = 'Test description',
            category = self.category,
            status = Product.Status.IN_STOCK,
            price = 100.00,
            quantity = 100
        )

    def test_create_order(self):
        self.client.force_authenticate(user = self.user)
        shopping_service = ShoppingService(self.client.session, 'cart')
        cart_service = CartService(shopping_service)

        cart_service.add(int(self.product.id), 2)

        order = OrderService.create_order(
            cart = cart_service,
            user = self.user,
            data = {
                'first_name': 'Artem',
                'last_name': 'Test',
                'phone': '+1234567890',
                'email': 'test@gmail.com',
                'address': 'Test address',
                'postal_code': '12345',
                'city': 'Test city',
            }
        )

        self.assertEqual(order.first_name, 'Artem')
        self.assertEqual(order.total_price(), 200.00)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 98)
        self.assertEqual(OrderItem.objects.filter(order = order).count(), 1)
        self.assertEqual(Order.Status.PENDING, order.status)

    def test_cancel_order(self):
        order = Order.objects.create(
            user = self.user,
            first_name = 'Artem',
            last_name = 'Test',
            phone = '+1234567890',
            email = 'test@gmail.com',
            address = 'Test address',
            postal_code = '12345',
            city = 'Test city',
        )
        order = OrderService.cancel_order(order = order)

        self.assertEqual(Order.Status.CANCELLED, order.status)

    def test_cancel_order_not_pending(self):
        order = Order.objects.create(
            user = self.user,
            first_name = 'Artem',
            phone = '+1234567890',
            email = 'test@gmail.com',
            address = 'Test address',
            postal_code = '12345',
            city = 'Test city',
        )
        order.status = Order.Status.PAID
        order.save()

        with self.assertRaises(Exception):
            OrderService.cancel_order(order = order)