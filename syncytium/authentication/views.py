from urllib.parse import urlencode

from account.models import RegistrationMethod
from account.serializers import UserSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .mixins import ApiErrorsMixin, PublicApiMixin
from .serializers import GoogleLoginInputSerializer
from .utils import (
    generate_tokens_for_user,
    google_get_access_token,
    google_get_user_info,
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

    def get(self, request):
        serializer = GoogleLoginInputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")

        login_url = f"{settings.BASE_FRONTEND_URL}/login"

        if error or not code:
            params = urlencode({"error": error})
            return redirect(f"{login_url}?{params}")

        redirect_uri = f"{settings.BASE_FRONTEND_URL}/google"
        access_token = google_get_access_token(code, redirect_uri)
        user_data = google_get_user_info(access_token)

        try:
            user = User.objects.get(email=user_data["email"])
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                "user": UserSerializer(user).data,
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            }
            return Response(response_data)

        except User.DoesNotExist:
            username = user_data["email"].split("@")[0]
            first_name = user_data.get("given_name", "")
            last_name = user_data.get("family_name", "")

            user = User.objects.create(
                username=username,
                email=user_data["email"],
                first_name=first_name,
                last_name=last_name,
                registration_method=RegistrationMethod.GOOGLE,
            )

            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                "user": UserSerializer(user).data,
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            }
            return Response(response_data)
