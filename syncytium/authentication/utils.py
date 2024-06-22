import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class GoogleOAuthUtils:
    """
    Utility class for Google OAuth2
    """

    class Constants:
        GOOGLE_ID_TOKEN_INFO_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
        GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
        GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    @classmethod
    def get_access_token(cls, code, redirect_uri):
        """
        Get access token from Google using the given code
        """
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(
            cls.Constants.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data
        )

        if not response.ok:
            raise ValidationError("Failed to obtain access token from Google.")

        access_token = response.json()["access_token"]

        return access_token

    @classmethod
    def get_user_info(cls, access_token):
        """
        Get user info from Google using the given access token
        """
        response = requests.get(
            cls.Constants.GOOGLE_USER_INFO_URL, params={"access_token": access_token}
        )

        if not response.ok:
            raise ValidationError("Failed to obtain user info from Google.")

        return response.json()


def generate_username_from_email(email):
    """
    Generate a username from the given email
    """
    prefix = email.split("@")[0]
    username = prefix
    suffix = 0
    while User.objects.filter(username=username).exists():
        username = f"{prefix}{suffix}"
        suffix += 1
    return username


def get_error_message(exc):
    """
    Get the error message from the given exception
    """
    return str(exc)


def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token
