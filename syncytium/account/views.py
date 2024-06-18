from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet

from .mixins import MustExistForUsernameAPIMixin
from .models import (
    UserAddress,
    UserEducation,
    UserEmailStatus,
    UserPrivacy,
    UserProfile,
    UserWorkExperience,
)
from .permissions import (
    CheckPrivacyPermission,
    IsCurrentUserOrReadOnlyPermission,
    IsCurrentUserPermission,
)
from .serializers import (
    UserAddressSerializer,
    UserEducationSerializer,
    UserPrivacySerializer,
    UserProfileSerializer,
    UserSerializer,
    UserWorkExperienceSerializer,
)
from .tasks import send_email_verification_link_email, send_registration_email

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    """
    API view to create a new user.
    """

    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data.pop("password")
        serializer.save()
        user = serializer.instance
        user.set_password(password)
        user.save()
        send_registration_email.delay(user.id)
        send_email_verification_link_email.delay(user.id, is_new=True)
        return user


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsCurrentUserPermission])
def get_email_token(request, username):
    """
    API view to get email token.
    """

    user = User.objects.filter(username=username).select_related("email_status").first()
    if not user:
        return Response({"detail": "User not found."}, status=HTTP_404_NOT_FOUND)
    if user.email_status.is_verified:
        return Response(
            {"detail": "Email is already verified."}, status=HTTP_400_BAD_REQUEST
        )
    send_email_verification_link_email.delay(user.id)
    return Response(
        {"detail": "Email verification link will be sent to you soon."},
        status=HTTP_200_OK,
    )


@api_view(["GET"])
def verify_email(request, token):
    """
    API view to verify email.
    """

    email_status = UserEmailStatus.objects.filter(verification_token=token).first()
    if not email_status:
        return Response({"detail": "Invalid link"}, status=HTTP_400_BAD_REQUEST)
    user = email_status.user
    last_email_status = (
        UserEmailStatus.objects.filter(user=user).order_by("-created").first()
    )
    if email_status.id != last_email_status.id:
        return Response(
            {"detail": "This is an old link, please open the newest link"},
            status=HTTP_400_BAD_REQUEST,
        )
    if last_email_status.is_verified:
        return Response(
            {"detail": "Email is already verified."}, status=HTTP_400_BAD_REQUEST
        )
    if not email_status.is_valid:
        return Response(
            {"detail": "This link has been expired. Please get a new one"},
            status=HTTP_400_BAD_REQUEST,
        )
    email_status.is_verified = True
    email_status.save()
    return Response({"detail": "Email verified successfully."}, status=HTTP_200_OK)


class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    API view to manage user profile.
    """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCurrentUserOrReadOnlyPermission,
        CheckPrivacyPermission,
    ]
    http_method_names = ["get", "patch"]
    privacy_field = "profile"
    model = UserProfile

    def get_object(self):
        return MustExistForUsernameAPIMixin.get_object(self, create=True)


class UserAddressAPIView(RetrieveUpdateAPIView):
    """
    API view to manage user address.
    """

    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCurrentUserOrReadOnlyPermission,
        CheckPrivacyPermission,
    ]
    http_method_names = ["get", "patch"]
    privacy_field = "address"
    model = UserAddress

    def get_object(self):
        return MustExistForUsernameAPIMixin.get_object(self, create=True)


class UserPrivacyAPIView(RetrieveUpdateAPIView):
    """
    API view to manage user privacy settings.
    """

    serializer_class = UserPrivacySerializer
    queryset = UserPrivacy.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCurrentUserOrReadOnlyPermission,
    ]
    http_method_names = ["get", "patch"]
    model = UserPrivacy

    def get_object(self):
        return MustExistForUsernameAPIMixin.get_object(self, create=True)


class UserEducationViewSet(ModelViewSet):
    """
    API view to manage user education.
    """

    serializer_class = UserEducationSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCurrentUserOrReadOnlyPermission,
        CheckPrivacyPermission,
    ]
    http_method_names = ["get", "post", "patch", "delete"]
    privacy_field = "education"
    model = UserEducation

    def get_queryset(self):
        username = self.kwargs.get("username")
        return self.model.objects.filter(user__username=username)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserWorkExperienceViewSet(ModelViewSet):
    """
    API view to manage user work experience.
    """

    serializer_class = UserWorkExperienceSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCurrentUserOrReadOnlyPermission,
        CheckPrivacyPermission,
    ]
    http_method_names = ["get", "post", "patch", "delete"]
    privacy_field = "work_experience"
    model = UserWorkExperience

    def get_queryset(self):
        username = self.kwargs.get("username")
        return self.model.objects.filter(user__username=username)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
