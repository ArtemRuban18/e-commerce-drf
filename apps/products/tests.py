from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.products.models import Product, Category
from django.contrib.auth.models import User

class ProductAPITestCase(APITestCase):
    def setUp(self):
        # Очищуємо продукти та категорії перед кожним тестом
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        
        self.super_user = User.objects.create_superuser(username='admin', password='testpwd')
        self.normal_user = User.objects.create_user(username='user', password='testpwd')
        self.category = Category.objects.create(name='Test')
        self.product = Product.objects.create(
            name='Test product',
            description='Test description',
            category=self.category,
            status=Product.Status.IN_STOCK,
            price=10.00,
            quantity=5
        )

        self.url = reverse('product-list')


    def test_get_products_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.product.name)

    def test_get_product_detail(self):
        url = reverse('product-detail', args=[self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)
    
    def test_create_product_as_normal_user(self):
        self.client.force_authenticate(user=self.normal_user)
        data = {
            'name': 'New product',
            'description': 'new description',
            'category': self.category.pk,
            'status': Product.Status.IN_STOCK,
            'price': 100,
            'quantity': 10,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_as_normal_user(self):
            self.client.force_authenticate(user=self.normal_user)
            url = reverse('product-detail', args=[self.product.slug])
            data = {
                'name': 'update product',
                'description': 'new description 2',
                'category': self.category.pk,
                'status': Product.Status.IN_STOCK,
                'price': 50,
                'quantity': 10,
            }
    
            response = self.client.put(url, data=data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_as_super_user(self):
        self.client.force_authenticate(user=self.super_user)
        data = {
            'name': 'New product 2',
            'description': 'new description 2',
            'category': self.category.pk,
            'status': Product.Status.IN_STOCK,
            'price': 50,
            'quantity': 10,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_product_as_super_user(self):
        self.client.force_authenticate(user=self.super_user)
        url = reverse('product-detail', args=[self.product.slug])
        data = {
            'name': 'update product 2',
            'description': 'new description 2',
            'category': self.category.pk,
            'status': Product.Status.IN_STOCK,
            'price': 50,
            'quantity': 10,
        }
    
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_out_of_stock_product(self):
        self.client.force_authenticate(user=self.super_user)
        url = reverse('product-detail', args=[self.product.slug])
        data = {
            'name': 'update product 2',
            'description': 'new description 2',
            'category': self.category.pk,
            'status': Product.Status.IN_STOCK,
            'price': 50,
            'quantity': 0,
        }

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Product.Status.OUT_OF_STOCK)
    
    def test_validate_price(self):
        self.client.force_authenticate(user=self.super_user)
        data = {
            'name': 'product 3',
            'description': 'description 3',
            'category': self.category.pk,
            'status': Product.Status.IN_STOCK,
            'price': -10,
            'quantity': 10,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_quantity(self):
        self.client.force_authenticate(user=self.super_user)
        data = {
            'name': 'product 3',
            'description': 'description 3',
            'category': self.category.pk,
            'status': Product.Status.IN_STOCK,
            'price': 10,
            'quantity': -5,
        }
    
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_status(self):
        self.client.force_authenticate(user=self.super_user)
        data = {
            'name': 'product 3',
            'description': 'description 3',
            'category': self.category.pk,
            'status': Product.Status.OUT_OF_STOCK,
            'price': 10,
            'quantity': 10,
        }
        
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)