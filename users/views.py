from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users import serializers


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""

    serializer_class = serializers.UserSerializer


class GenerateTokenView(ObtainAuthToken):
    """Generate a new authentication token for a user"""

    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
