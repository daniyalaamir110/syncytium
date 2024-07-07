from account.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Relation, UserRelation

User = get_user_model()


class UserRelationWriteSerializer(serializers.ModelSerializer):
    """Serializer for the `UserRelation` model"""

    class Meta:
        model = UserRelation
        fields = ["to", "relation"]

    def validate(self, data):
        if self.context["request"].user.id == data["to"].id:
            raise serializers.ValidationError(
                "You cannot create a relation with yourself"
            )
        if UserRelation.objects.existing_user_relation(
            self.context["request"].user, data["to"], data["relation"]
        ).exists():
            raise serializers.ValidationError("The relation already exists")
        return data


class UserRelationReadSerializer(serializers.ModelSerializer):
    """Serializer for the `UserRelation` model"""

    related_user = serializers.SerializerMethodField()

    class Meta:
        model = UserRelation
        fields = ["relation", "related_user", "created", "modified"]
        read_only_fields = ["related_user"]

    def get_related_user(self, obj):
        user = (
            obj.user
            if self.context["request"].user.id == obj.to.id
            else obj.to if obj.relation == Relation.FRIEND else obj.to
        )
        return UserSerializer(user).data
