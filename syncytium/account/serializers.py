from core.utils import validate_country_and_city
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    validate_password as validate_password_django,
)
from rest_framework import serializers

from .models import (
    UserAddress,
    UserEducation,
    UserPrivacy,
    UserProfile,
    UserWorkExperience,
)

User = get_user_model()


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


class UserPrivacySerializer(serializers.ModelSerializer):
    """
    User privacy serializer
    """

    class Meta:
        model = UserPrivacy
        fields = [
            "id",
            "user",
            "profile",
            "address",
            "education",
            "work_experience",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User profile serializer
    """

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "bio",
            "birth_date",
            "website",
            "phone",
            "avatar",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }


class UserAddressSerializer(serializers.ModelSerializer):
    """
    User address serializer
    """

    class Meta:
        model = UserAddress
        fields = [
            "id",
            "user",
            "country",
            "city",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        city = attrs.get("city")
        country = attrs.get("country")
        if city:
            country, city = validate_country_and_city(country, city)
        attrs["country"] = country
        attrs["city"] = city
        return attrs


class UserEducationSerializer(serializers.ModelSerializer):
    """
    User education serializer
    """

    class Meta:
        model = UserEducation
        fields = [
            "id",
            "user",
            "school",
            "degree",
            "field_of_study",
            "start_date",
            "end_date",
            "description",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }


class UserWorkExperienceSerializer(serializers.ModelSerializer):
    """
    User work experience serializer
    """

    class Meta:
        model = UserWorkExperience
        fields = [
            "id",
            "user",
            "company",
            "position",
            "start_date",
            "end_date",
            "description",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }
