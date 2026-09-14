from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Order, OrderItem
from apps.products.models import Product, Category
from .services import OrderService
from django.contrib.auth.models import User
from apps.shopping.services import ShoppingService, CartService

class OrderServiceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password = 'testpassword')
        self.category = Category.objects.create(name = 'test')
        self.product = Product.objects.create(
            name = 'Test product',
            description = 'Test description',
            categroy = self.category,
            status = Product.Status.IN_STOCK,
            price = 100.00,
            quantity = 100
        )

        self.url = reverse('order')

    def test_create_order(self):
        self.client.force_authenticate(user = self.user)
        shopping_service = ShoppingService(self.client.session, 'cart')
        cart_service = CartService(shopping_service)

        cart_service.add(int(self.product.id, 2))

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
        self.assertEqal(order.total_price, 200.00)
        response = self.client.get(reverse('order', kwargs = {'pk': order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
                                   
        
