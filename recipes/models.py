from django.conf import settings
from django.db import models


class Recipe(models.Model):
    """Database model for recipes"""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    cooking_time = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
