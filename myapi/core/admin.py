from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RoadsideCallout, UserSubscriptions, UserLocation

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'user_type', 'image'
        )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RoadsideCallout)
admin.site.register(UserSubscriptions)
admin.site.register(UserLocation)
