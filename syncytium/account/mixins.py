from .models import (
    UserProfile,
    UserPrivacy,
    UserAddress,
    UserEducation,
    UserWorkExperience,
)
from core.models import Privacy
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS


class DetailMustBeCurrentUserAPIMixin:
    """
    Mixin to check if the detail object is the current user.
    If the object is not the current user, raise a 404 error.
    """

    def is_current_user(self, username):
        if self.request.user.username != username:
            raise PermissionDenied(
                "You do not have permission to access this resource."
            )

    def is_current_user_from_username_kwarg(self):
        username = self.kwargs.get("username")
        self.is_current_user(username)


class MustExistForUsernameAPIMixin:
    """
    Mixin to check if the detail object exists.
    - The `model` attribute must be defined in the view.
    - In case of read-only methods, if the object does not exist, raise a 404 error.
    - In case of write methods, if the object does not exist, create it if `create` is `True`.
    """

    def get_object(self, create=False):
        username = self.kwargs.get("username")
        try:
            return self.model.objects.get(user__username=username)
        except self.model.DoesNotExist:
            if self.request.method in SAFE_METHODS or not create:
                raise NotFound
            return self.model(user_id=self.request.user.id)


class CheckPrivacyAPIMixin:
    """
    Mixin to check if the privacy settings allow access to the field.
    If the field is private, raise a 403 error.
    """

    def check_privacy(self, username, field):
        current_user = self.request.user
        if current_user.username == username:
            return
        privacy = UserPrivacy.objects.filter(user__username=username).first()
        if privacy:
            if getattr(privacy, field) == Privacy.PRIVATE:
                raise PermissionDenied(
                    "You don't have permission to access this resource."
                )

    def check_privacy_from_username_kwarg(self, field):
        username = self.kwargs.get("username")
        self.check_privacy(username, field)
