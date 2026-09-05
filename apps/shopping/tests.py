from rest_framework.test import APITestCase
from .services import CartService, WishlistService, ShoppingService
from apps.products.models import Product, Category
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
class CartServiceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            name='Test product',
            description='Test description',
            category=self.category,
            status=Product.Status.IN_STOCK,
            price=10.00,
            quantity=5
        )

        self.url = reverse('cart')

    def test_add_product_to_cart(self):
        self.client.force_authenticate(user=self.user)
        shopping_service = ShoppingService(self.client.session, 'cart')
        cart_service = CartService(shopping_service)
        cart_service.add(int(self.product.id), 2)
        self.assertEqual(cart_service.get_items(), {str(self.product.id): 2})

    def test_update_product_quantity_in_cart(self):
        self.client.force_authenticate(user=self.user)
        shopping_service = ShoppingService(self.client.session, 'cart')
        cart_service = CartService(shopping_service)
        cart_service.add(int(self.product.id), 2)
        cart_service.update(int(self.product.id), 3)
        self.assertEqual(cart_service.get_items(), {str(self.product.id): 3})

    def test_remove_product_from_cart(self):
        self.client.force_authenticate(user=self.user)
        shopping_service = ShoppingService(self.client.session, 'cart')
        cart_service = CartService(shopping_service)
        cart_service.add(int(self.product.id), 2)
        cart_service.remove(int(self.product.id))
        self.assertEqual(cart_service.get_items(), {})

    def test_clear_cart(self):
        self.client.force_authenticate(user=self.user)
        shopping_service = ShoppingService(self.client.session, 'cart')
        cart_service = CartService(shopping_service)
        cart_service.add(int(self.product.id), 2)
        cart_service.clear()
        self.assertEqual(cart_service.get_items(), {})
    
    def test_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_cart(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, {
            'product_id': self.product.id,
            'quantity': 2
        }, format='json')
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['name'], self.product.name)
        self.assertEqual(response.data['items'][0]['quantity'], 2)


class WishlistServiceTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            name='Test product',
            description='Test description',
            category=self.category,
            status=Product.Status.IN_STOCK,
            price=10.00,
            quantity=5
        )

        self.url = reverse('wishlist')

    def test_add_product_to_wishlist(self):
        self.client.force_authenticate(user=self.user)
        shopping_service = ShoppingService(self.client.session, 'wishlist')
        wishlist_service = WishlistService(shopping_service)
        wishlist_service.add(int(self.product.id))
        self.assertEqual(wishlist_service.get_items(), {str(self.product.id): 1})

    def test_remove_product_from_wishlist(self):
        self.client.force_authenticate(user=self.user)
        shopping_service = ShoppingService(self.client.session, 'wishlist')
        wishlist_service = WishlistService(shopping_service)
        wishlist_service.add(int(self.product.id))
        wishlist_service.remove(int(self.product.id))
        self.assertEqual(wishlist_service.get_items(), {})

    def test_clear_wishlist(self):
        self.client.force_authenticate(user=self.user)
        shopping_service = ShoppingService(self.client.session, 'wishlist')
        wishlist_service = WishlistService(shopping_service)
        wishlist_service.add(int(self.product.id))
        wishlist_service.clear()
        self.assertEqual(wishlist_service.get_items(), {})
    
    def test_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_wishlist(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.url, {
            'product_id': self.product.id
        }, format='json')
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['name'], self.product.name)
        self.assertEqual(response.data['total_quantity'], 1)