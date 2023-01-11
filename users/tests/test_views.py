from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class PublicUserApiTestCase(TestCase):
    """Test public features of user API"""

    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        self.create_user_url = reverse("users:register")
        self.user_data = {
            "email": "user@example.com",
            "name": "John Doe",
            "password": "qwerty12345",
        }

    def test_create_user_success(self):
        """Test creating a new user is successful"""
        resp = self.client.post(self.create_user_url, self.user_data)
        user = self.user_model.objects.get(email=self.user_data["email"])

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertNotIn("password", resp.data)

    def test_create_user_email_exists_fail(self):
        """Test creating a new user with an existing email fails"""
        self.user_model.objects.create_user(**self.user_data)
        resp = self.client.post(self.create_user_url, self.user_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_too_short_fail(self):
        """Test creating a new user with too short password fails"""
        self.user_data["password"] = "pw"
        resp = self.client.post(self.create_user_url, self.user_data)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            self.user_model.objects.filter(email=self.user_data["email"]).exists()
        )
