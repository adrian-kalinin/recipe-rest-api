from rest_framework import serializers

from recipes import models


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    class Meta:
        model = models.Recipe
        fields = ("id", "title", "cooking_time", "description")
        read_only_fields = ("id",)
