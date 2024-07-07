from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserRelationViewSet

router = DefaultRouter()
router.register(r"", UserRelationViewSet, basename="user-relations")

urlpatterns = []

urlpatterns += router.urls
