from django.contrib import admin

from .models import (
    UserAddress,
    UserEducation,
    UserEmailStatus,
    UserPrivacy,
    UserProfile,
    UserWorkExperience,
)

admin.site.register(UserAddress)
admin.site.register(UserEducation)
admin.site.register(UserPrivacy)
admin.site.register(UserProfile)
admin.site.register(UserWorkExperience)
admin.site.register(UserEmailStatus)
