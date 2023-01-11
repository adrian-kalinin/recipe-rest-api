from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users"""

    def create(self, validated_data):
        """Create and return a new user with encrypted password"""
        return self.Meta.model.objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields = ("email", "name", "password")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
