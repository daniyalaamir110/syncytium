from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    validate_password as validate_password_django,
)


class UserSerializer(serializers.ModelSerializer):
    """
    User create serializer
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=20,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
        }

    def validate_password(self, password):
        validate_password_django(password)
        return password

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use")
        return email
