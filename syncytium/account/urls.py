from django.urls import path, re_path
from .views import (
    UserCreateAPIView,
    UserPrivacyAPIView,
    UserProfileAPIView,
    UserAddressAPIView,
    UserEducationViewSet,
    UserWorkExperienceViewSet,
)

app_name = "account"

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register_user"),
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
