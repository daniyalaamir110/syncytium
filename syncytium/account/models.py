from core.models import Privacy, TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F
from django.db.models.functions import ExtractSecond, Greatest, Now
from django.utils import timezone

User = get_user_model()

# Make email field unique, blank and null fields false
User._meta.get_field("email")._unique = True
User._meta.get_field("email").blank = False
User._meta.get_field("email").null = False


class UserPrivacy(TimeStampedModel):
    """
    This model stores the user privacy settings.
    Initially, it only contains the user field, which is a one-to-one
    field to the default Django user model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="privacy")
    profile = models.CharField(
        choices=Privacy.choices, default=Privacy.PUBLIC, max_length=2
    )
    address = models.CharField(
        choices=Privacy.choices, default=Privacy.PUBLIC, max_length=2
    )
    education = models.CharField(
        choices=Privacy.choices, default=Privacy.PUBLIC, max_length=2
    )
    work_experience = models.CharField(
        choices=Privacy.choices, default=Privacy.PUBLIC, max_length=2
    )

    class Meta:
        verbose_name_plural = "User privacies"

    def __str__(self):
        return f"{self.user.username} privacy settings"


EMAIL_TOKEN_VALIDITY = 1


class UserEmailStatus(TimeStampedModel):
    """
    This model stores the user email status.
    Initially, it only contains the user field, which is a one-to-one
    field to the default Django user model.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="email_status"
    )
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=32, blank=True)

    @property
    def is_valid(self):
        """
        Check if the email status is valid.
        Used token is always invalid.
        Only the last token is be valid, if not verified.
        """
        if self.is_verified:
            return False
        last_email_status = (
            UserEmailStatus.objects.filter(user=self.user).order_by("-created").first()
        )
        if self.id == last_email_status.id:
            created = self.created
            now = timezone.now()
            if (now - created).days < EMAIL_TOKEN_VALIDITY:
                return True
        return False

    def __str__(self):
        return f"{self.user.username} email status"

    class Meta:
        verbose_name_plural = "User email statuses"


class UserProfile(TimeStampedModel):
    """
    This model extends the default Django user model.
    Initially, it only contains the user field, which is a one-to-one
    field to the default Django user model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date of birth")
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)

    def __str__(self):
        return self.user.username


class UserAddress(TimeStampedModel):
    """
    This model stores the user address.
    Initially, it only contains the user field, which is a one-to-one
    field to the default Django user model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
    country = models.ForeignKey(
        "cities_light.Country", on_delete=models.SET_NULL, null=True, blank=True
    )
    city = models.ForeignKey(
        "cities_light.City", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "User addresses"

    def __str__(self):
        return f"{self.user.username} lives in {self.city.name}, {self.country.name}"


class UserEducation(TimeStampedModel):
    """
    This model stores the user education information.
    Initially, it only contains the user field, which is a one-to-one
    field to the default Django user model.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="educations")
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255, verbose_name="Field of study")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} studied {self.field_of_study} at {self.school}"


class UserWorkExperience(TimeStampedModel):
    """
    This model stores the user work experience information.
    Initially, it only contains the user field, which is a one-to-one
    field to the default Django user model.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="work_experiences"
    )
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} worked as a {self.position} at {self.company}"
