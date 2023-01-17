from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipes import models, serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for recipes"""

    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(author=self.request.user).order_by("-id")
