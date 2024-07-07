from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created` and `modified` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Privacy(models.TextChoices):
    """Choices for the privacy settings"""
    PUBLIC = "PU", "Public"
    PRIVATE = "PR", "Private"
    FRIENDS = "FR", "Friends"
