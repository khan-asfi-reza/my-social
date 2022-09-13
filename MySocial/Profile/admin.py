from django.contrib import admin

from .models import (
    Profile,
)


# Profile Admin Panel
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'online',)


admin.site.register(Profile, ProfileAdmin)
