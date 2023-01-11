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
