from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from recipes import models, serializers

User = get_user_model()


class PublicRecipeApiTestCase(TestCase):
    """Test public features of recipe API"""

    def setUp(self):
        self.client = APIClient()
        self.recipe_url = reverse("recipes:recipe-list")

    def test_auth_required(self):
        """Test authentication is required to call API"""
        resp = self.client.get(self.recipe_url)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTestCase(TestCase):
    """Test private features of recipe API"""

    def setUp(self):
        self.client = APIClient()
        self.recipe_url = reverse("recipes:recipe-list")
        self.user = User.objects.create_user(
            email="user@example.com",
            name="John Doe",
            password="qwerty12345",
        )
        self.recipe_data = {
            "user": self.user,
            "title": "Pasta",
            "cooking_time": 20,
            "description": "Lorem ipsum dolor sit amet",
        }
        self.client.force_authenticate(self.user)

    def test_list_recipes(self):
        """Test retrieving a list of recipes"""
        models.Recipe.objects.create(**self.recipe_data)
        models.Recipe.objects.create(**self.recipe_data)

        resp = self.client.get(self.recipe_url)

        recipes = models.Recipe.objects.all().order_by("-id")
        serializer = serializers.Recipe(recipes, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_list_recipes_limited_to_user(self):
        """Test retrieving a list of recipes limited to user"""
        other_user = User.objects.create_user(
            email="other@example.com", password="asdf6789"
        )
        models.Recipe.objects.create(**self.recipe_data)
        models.Recipe.objects.create(**self.recipe_data, user=other_user)

        resp = self.client.get(self.recipe_url)

        recipes = models.Recipe.objects.filter(user=self.user)
        serializer = serializers.Recipe(recipes, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)
