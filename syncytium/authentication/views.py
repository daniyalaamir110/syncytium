from urllib.parse import urlencode

from account.models import RegistrationMethod
from account.serializers import UserSerializer
from account.tasks import send_registration_email
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .mixins import ApiErrorsMixin, PublicApiMixin
from .serializers import GoogleLoginInputSerializer
from .utils import (
    GoogleOAuthUtils,
    generate_tokens_for_user,
    generate_username_from_email,
)

User = get_user_model()


class CurrentUserRetrieveAPIView(RetrieveAPIView):
    """
    API view to retrieve the current user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @action(detail=False, methods=["GET"])
    def retrieve(self, request):
        user = self.get_serializer(request.user).data
        return Response(user, status=HTTP_200_OK)


class GoogleLoginAPIView(APIView, ApiErrorsMixin, PublicApiMixin):
    """
    API view to login with Google.
    """

    @extend_schema(
        parameters=[
            OpenApiParameter(name="code", type=str),
            OpenApiParameter(name="error", type=str),
        ],
    )
    def get(self, request):
        serializer = GoogleLoginInputSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")

        login_url = f"{settings.BASE_FRONTEND_URL}/login"

        if error or not code:
            params = urlencode({"error": error})
            return redirect(f"{login_url}?{params}")

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/google"

        try:
            access_token = GoogleOAuthUtils.get_access_token(code, redirect_uri)
        except:
            return Response(
                {"detail": "Could not get access token from Google."},
                HTTP_400_BAD_REQUEST,
            )

        try:
            user_data = GoogleOAuthUtils.get_user_info(access_token)
        except:
            return Response(
                {"detail": "Could not get user info from Google."},
                HTTP_400_BAD_REQUEST,
            )

        email = user_data["email"]
        user = User.objects.filter(email=email).first()

        if not user:
            username = generate_username_from_email(email)
            first_name = user_data.get("given_name", "")
            last_name = user_data.get("family_name", "")

            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                registration_method=RegistrationMethod.GOOGLE,
            )
            send_registration_email.delay(user.id)

        elif user.registration_method != RegistrationMethod.GOOGLE:
            return Response(
                {"detail": "Please login with password."},
                HTTP_400_BAD_REQUEST,
            )

        access_token, refresh_token = generate_tokens_for_user(user)
        response_data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
        }
        return Response(response_data)
