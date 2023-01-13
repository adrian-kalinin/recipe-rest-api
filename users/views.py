from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users import serializers


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""

    serializer_class = serializers.UserSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    """Retrieve or update authenticated user"""

    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class GenerateTokenView(ObtainAuthToken):
    """Generate a new authentication token for a user"""

    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
