from django.contrib import admin
from .models import (
    UserAddress,
    UserEducation,
    UserPrivacy,
    UserProfile,
    UserWorkExperience,
    UserEmailStatus,
)

# Register your models here.
admin.site.register(UserAddress)
admin.site.register(UserEducation)
admin.site.register(UserPrivacy)
admin.site.register(UserProfile)
admin.site.register(UserWorkExperience)
admin.site.register(UserEmailStatus)
