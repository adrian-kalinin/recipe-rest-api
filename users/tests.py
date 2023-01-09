from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTestCase(TestCase):
    """Test users app on admin site"""

    def setUp(self):
        """Set up initial data"""
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email="user@example.com", password="qwerty12345", name="John Doe"
        )
        self.superuser = self.user_model.objects.create_superuser(
            email="admin@example.com", password="qwerty12345"
        )
        self.client.force_login(self.superuser)

    def test_list_users_page(self):
        """Test list users page"""
        url = reverse("admin:users_user_changelist")
        resp = self.client.get(url)

        self.assertContains(resp, self.user.name)
        self.assertContains(resp, self.user.email)

    def test_edit_user_page(self):
        """Test edit user page"""
        url = reverse("admin:users_user_change", args=[self.user.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_create_user_page(self):
        """Test create user page"""
        url = reverse("admin:users_user_add")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)


class UserModelTestCase(TestCase):
    """Test User model"""

    def setUp(self):
        """Set up initial data"""
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
