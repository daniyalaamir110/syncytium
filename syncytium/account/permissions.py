from core.models import Privacy
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import UserPrivacy


def get_privacy(username, field):
    """
    Get the privacy settings for the user and field.

    Operations:
    - Filter the privacy settings by the user's username, and return the
    value of the provided field.
    - If the privacy settings are not found, assume public access.

    Returns:
        `str`: `"PR" | "PU" | "FR"`
    """
    privacy = UserPrivacy.objects.filter(user__username=username).first()
    if privacy:
        return getattr(privacy, field)
    return Privacy.PUBLIC


class IsCurrentUserPermission(BasePermission):
    """
    Permission class to check if the current user is the same as the user
    in the URL.

    Operations:
    - If the current user is the same as the user in the URL, allow access.
    - If the current user is not the same as the user in the URL, deny access.

    Raises:
    - `PermissionDenied`: If the current user is not the same as the user in the URL.
    """

    def has_permission(self, request, view):
        username = view.kwargs.get("username")
        current_user = request.user
        is_current_user = current_user.username == username
        if is_current_user:
            return True
        raise PermissionDenied("You do not have permission to access this resource.")


class IsCurrentUserOrReadOnlyPermission(IsCurrentUserPermission):
    """
    Permission class to check if the current user is the same as the user
    in the URL. If the user is not the same, only allow read-only methods.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class CheckPrivacyPermission(BasePermission):
    """
    Permission class to check the privacy settings for a user.

    Operations:
    - Only applies to read-only methods. For write methods, it is always `True`.
    - The `privacy_field` attribute must be defined in the view.
    - If the current user is the same as the user in the URL, allow access.
    - If the privacy settings are public, allow access.
    - If the privacy settings are private, deny access.
    - If the privacy settings are friends, allow access only if current user
    is one of the user's friends.

    Raises:
    - `PermissionDenied`: If the current user does not have permission to access
    """

    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return True
        username = view.kwargs.get("username")
        current_user = request.user
        is_current_user = current_user.username == username
        if is_current_user:
            return True
        privacy = get_privacy(username, view.privacy_field)
        if privacy == Privacy.PUBLIC:
            return True
        raise PermissionDenied("You don't have permission to access this resource.")
