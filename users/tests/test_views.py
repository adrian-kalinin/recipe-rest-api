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
        self.profile_url = reverse("users:profile")
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

    def test_retrieve_profile_user_unauthorized_fail(self):
        """Test retrieving profile with unauthenticated user fails"""
        resp = self.client.get(self.profile_url)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTestCase(TestCase):
    """Test private features of user API"""

    def setUp(self):
        self.client = APIClient()
        self.profile_url = reverse("users:profile")
        self.user = User.objects.create_user(
            email="user@example.com",
            name="John Doe",
            password="qwerty12345",
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged-in user is successful"""
        resp = self.client.get(self.profile_url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, {"email": self.user.email, "name": self.user.name})

    def test_partial_update_profile_success(self):
        """Test partially updating profile for logged-in user is successful"""
        data = {"name": "Jane Roe", "password": "asdf6789"}
        resp = self.client.patch(self.profile_url, data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data["name"])
        self.assertTrue(self.user.check_password(data["password"]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
