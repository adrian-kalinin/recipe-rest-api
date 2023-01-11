from rest_framework import generics

from users import serializers


class CreateUserView(generics.CreateAPIView):
    """Creates a new user"""

    serializer_class = serializers.UserSerializer
