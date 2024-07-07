from core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F
from django.db.models.constraints import CheckConstraint

User = get_user_model()


class Relation(models.TextChoices):
    """Choices for the relation types"""

    FRIEND = "FR", "Friend"
    FOLLOWER = "FO", "Follower"
    BLOCKED = "BL", "Blocked"


class UserRelationQuerySet(models.QuerySet):
    """Custom queryset for the `UserRelation` model"""

    def bdfilter(self, user):
        """
        Filter the relations for both users i.e. bidirectional filter
        from `user` and `to` fields

        Args:
            `user` (`User`): The user instance

        Returns:
            `Self@UserRelationQuerySet`: The filtered queryset
        """
        return self.filter(Q(user=user) | Q(to=user))

    def user_relations(self, user, relation=None):
        """
        Get the user's relations

        Operations:
        - If the relation is FRIEND, filter the relations for both users.
        - If the relation is not FRIEND, filter the relations for the user.

        Args:
            `user` (`User`): The user instance
            `relation` (`"FR" | "FO" | "BL" | None`): The relation type

        Returns:
            `Self@UserRelationQuerySet`: The filtered queryset
        """
        queryset = self.filter(relation=Relation.FRIEND).bdfilter(
            user=user
        ) | self.exclude(relation=Relation.FRIEND).filter(user=user)
        if relation:
            return queryset.filter(relation=relation)
        return queryset

    def existing_user_relation(self, user, to, relation):
        """
        Get the existing relation between two users

        Args:
            `user` (`User`): The user instance
            `to` (`User`): The related user instance
            `relation` (`str`): The relation type

        Returns:
            `Self@UserRelationQuerySet`: The filtered queryset
        """
        relations = self.user_relations(user, relation)
        return (
            relations.bdfilter(user=to)
            if relation == Relation.FRIEND
            else relations.filter(to=to)
        )


class UserRelationManager(models.Manager):
    """Custom manager for the `UserRelation` model"""

    def get_queryset(self):
        return UserRelationQuerySet(self.model, using=self._db)


class UserRelation(TimeStampedModel):
    """
    This model stores the user relationships.

    Initially, it only contains the user and friend fields, which are
    foreign keys to the default Django user model.
    """

    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="relations"
    )
    to = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="related_to"
    )
    relation = models.CharField(
        choices=Relation.choices, default=Relation.FRIEND, max_length=2
    )

    objects = UserRelationManager()

    class Meta:
        unique_together = ["user", "to", "relation"]
        verbose_name_plural = "User relations"
        constraints = [
            CheckConstraint(
                check=~Q(user=F("to")),
                name="user_and_to_not_equal",
                violation_error_message="You cannot create a relation with yourself",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} is {self.relation} with {self.friend.username}"
