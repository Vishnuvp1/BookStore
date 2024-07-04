from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterViewTestCase(APITestCase):
    def test_register_user(self):
        url = reverse("register")
        data = {"username": "testuser", "password": "1234", "email": "user@gmail.com"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "User created successfully")

    def test_register_invalid_data(self):
        url = reverse("register")
        data = {}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login(self):
        url = reverse("login")
        data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        url = reverse("login")
        data = {
            "username": "testuser",
            "password": "wrongpassword",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_credentials(self):
        url = reverse("login")
        data = {}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_token_creation(self):
        url = reverse("login")
        data = {
            "username": "testuser",
            "password": "testpassword",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data["token"], token.key)
