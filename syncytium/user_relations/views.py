from core.paginators import CustomPageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import UserRelation
from .serializers import UserRelationReadSerializer, UserRelationWriteSerializer


class UserRelationViewSet(ModelViewSet):
    """ViewSet for the `UserRelation` model"""

    queryset = UserRelation.objects.all().select_related("user", "to")
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "related_user__username",
        "related_user__full_name",
        "related_user__email",
    ]
    http_method_names = ["get", "post", "delete"]

    def get_serializer_class(self):
        read = self.request.method in SAFE_METHODS
        return UserRelationReadSerializer if read else UserRelationWriteSerializer

    def filter_queryset(self, queryset):
        relation = self.request.GET.get("relation")
        return queryset.user_relations(self.request.user, relation)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
