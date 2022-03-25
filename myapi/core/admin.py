from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RoadsideCallout

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'user_type'
        )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RoadsideCallout)
