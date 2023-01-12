from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class PublicUserApiTestCase(TestCase):
    """Test public features of user API"""

    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse("users:register")
        self.retrieve_token_url = reverse("users:login")
        self.user_data = {
            "email": "user@example.com",
            "name": "John Doe",
            "password": "qwerty12345",
        }

    def test_create_user_success(self):
        """Test creating a new user is successful"""
        resp = self.client.post(self.create_user_url, self.user_data)
        user = User.objects.get(email=self.user_data["email"])

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertNotIn("password", resp.data)

    def test_create_user_email_exists_fail(self):
        """Test creating a new user with an existing email fails"""
        User.objects.create_user(**self.user_data)
        resp = self.client.post(self.create_user_url, self.user_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short_fail(self):
        """Test creating a new user with too short password fails"""
        self.user_data["password"] = "pw"
        resp = self.client.post(self.create_user_url, self.user_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email=self.user_data["email"]).exists())

    def test_retrieve_token_success(self):
        """Test retrieving token for valid credentials is successful"""
        User.objects.create_user(**self.user_data)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        resp = self.client.post(self.retrieve_token_url, login_data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("token", resp.data)

    def test_retrieve_token_bad_credentials_fail(self):
        """Test retrieving token with bad credentials fails"""
        User.objects.create_user(**self.user_data)
        login_data = {
            "email": "test@example.com",
            "password": "password",
        }
        resp = self.client.post(self.retrieve_token_url, login_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", resp.data)

    def test_retrieve_token_blank_password_fail(self):
        """Test retrieving token with blank password fails"""
        User.objects.create_user(**self.user_data)
        login_data = {
            "email": "test@example.com",
            "password": "",
        }
        resp = self.client.post(self.retrieve_token_url, login_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", resp.data)
