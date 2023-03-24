from rest_framework import serializers

from reviews.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError('Никнейм "me" запрещён')
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenAproveSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
