from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test User model"""

    def test_create_user_with_email_success(self):
        """Test creating a user with an email is successful"""
        user_data = {
            "email": "user@example.com",
            "password": "qwerty12345",
        }
        user = User.objects.create_user(**user_data)

        self.assertEqual(user.email, user_data["email"])
        self.assertTrue(user.check_password(user_data["password"]))

    def test_create_user_and_normalize_email(self):
        """Test email is normalized for new users"""
        sample_emails = (
            ("first@EXAMPLE.COM", "first@example.com"),
            ("SECOND@example.com", "SECOND@example.com"),
            ("THIRD@EXAMPLE.COM", "THIRD@example.com"),
            ("forth@example.com", "forth@example.com"),
        )

        for email, expected in sample_emails:
            user = User.objects.create_user(email=email)
            self.assertEqual(user.email, expected)

    def test_create_user_without_email_fail(self):
        """Test creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            User.objects.create_user("", "qwerty12345")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = User.objects.create_superuser(
            email="user@example.com",
            password="qwerty12345",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
