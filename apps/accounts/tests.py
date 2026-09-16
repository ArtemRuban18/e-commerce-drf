from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.accounts.serializers import RegisterSerializer
from rest_framework import status

class RegisterSerializerTestCase(APITestCase):
    def test_register_serilaizer_valid_data(self):
        data = {
            "username": "testuser",
            "email": "testemail@gmail.com",
            "password": "testpwd",
            "password2": "testpwd"
        }
        serializer = RegisterSerializer(data = data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_invalid_data(self):
        data = {
            "username": "testuser",
            "email": "testemail@gmail.com",
            "password": "testpwd",
            "password2": "wrongpwd"
        }
        serializer = RegisterSerializer(data = data)
        self.assertFalse(serializer.is_valid())
    
    def test_register_serializer_dublicate_email(self):
        user = User.objects.create_user(username = "usertest", email="test@gmail.com", password="testpwd")
        user.refresh_from_db()
        data = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "testpwd",
            "password2": "testpwd"
        }
        serializer = RegisterSerializer(data = data)
        self.assertFalse(serializer.is_valid())

class RegisterAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("register")

    def test_create_user(self):
        data = {
            "username": "testuser",
            "email": "testemail@gmail.com",
            "password": "testpwd",
            "password2": "testpwd"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username = "testuser").exists())

    def test_create_user_with_wrong_password_confirmation(self):
        data = {
            "username": "testuser",
            "email": "testemail@gmail.com",
            "password": "testpwd",
            "password2": "wrongpwd"
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username = "testuser").exists())

    def test_create_user_with_dublicate_email(self):
        user = User.objects.create_user(username="new_user", email="test@gmail.com", password="testpwd")
        user.refresh_from_db()
        data = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "testpwd",
            "password2": "testpwd"
        }

        response = self.client.post(self.url, data)
        self.assertFalse(User.objects.filter(username="testuser").exists())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
