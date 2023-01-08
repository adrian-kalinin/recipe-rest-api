from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTestCase(TestCase):
    """Test User model"""

    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "user@example.com"
        password = "qwerty12345"

        user = self.user_model.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_and_normalize_email(self):
        """Test email is normalized for new users"""
        sample_emails = (
            ("first@EXAMPLE.COM", "first@example.com"),
            ("SECOND@example.com", "SECOND@example.com"),
            ("THIRD@EXAMPLE.COM", "THIRD@example.com"),
            ("forth@example.com", "forth@example.com"),
        )

        for email, expected in sample_emails:
            user = self.user_model.objects.create_user(email=email)
            self.assertEqual(user.email, expected)

    def test_create_user_without_email_fail(self):
        """Test creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user("", "qwerty12345")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = self.user_model.objects.create_superuser(
            email="user@example.com",
            password="qwerty12345",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
