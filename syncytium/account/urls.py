from django.urls import path, re_path

from .views import (
    UserAddressAPIView,
    UserChangeEmailAPIView,
    UserCreateAPIView,
    UserEducationViewSet,
    UserPrivacyAPIView,
    UserProfileAPIView,
    UserWorkExperienceViewSet,
    get_email_token,
    verify_email,
)

app_name = "account"

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register_user"),
    re_path(
        r"(?P<username>[\w.@+-]+)/email-token/$",
        get_email_token,
        name="user_email_token",
    ),
    re_path(
        r"verify-email/(?P<token>[\w.@+-]+)/$",
        verify_email,
        name="verify_email",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/change-email/$",
        UserChangeEmailAPIView.as_view(),
        name="change_email",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/privacy/$",
        UserPrivacyAPIView.as_view(),
        name="user_privacy",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/profile/$",
        UserProfileAPIView.as_view(),
        name="user_profile",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/address/$",
        UserAddressAPIView.as_view(),
        name="user_address",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/education/$",
        UserEducationViewSet.as_view({"get": "list", "post": "create"}),
        name="user_education",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/education/(?P<pk>\d+)/$",
        UserEducationViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="user_education_detail",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/work-experience/$",
        UserWorkExperienceViewSet.as_view({"get": "list", "post": "create"}),
        name="user_work_experience",
    ),
    re_path(
        r"(?P<username>[\w.@+-]+)/work-experience/(?P<pk>\d+)/$",
        UserWorkExperienceViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
        name="user_work_experience",
    ),
]
