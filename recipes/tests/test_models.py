from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes import models

User = get_user_model()


class RecipeModelTestCase(TestCase):
    """Test Recipe model"""

    def test_create_recipe(self):
        """Test creating a recipe is successful"""
        user = User.objects.create_user(
            email="test@example.com",
            password="qwerty12345",
        )
        recipe = models.Recipe.objects.create(
            author=user,
            title="Pasta",
            cooking_time=5,
            description="Lorem ipsum dolor sit amet",
        )

        self.assertEqual(str(recipe), recipe.title)
