from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    UserSerializer,
    UserPrivacySerializer,
    UserProfileSerializer,
    UserAddressSerializer,
    UserEducationSerializer,
    UserWorkExperienceSerializer,
)
from .models import (
    UserPrivacy,
    UserProfile,
    UserAddress,
    UserEducation,
    UserWorkExperience,
)
from .mixins import MustExistForUsernameAPIMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsCurrentUserOrReadOnlyPermission, CheckPrivacyPermission


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
        UserPrivacy.objects.create(user=user)
        return user


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
