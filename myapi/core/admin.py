from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RoadsideCallout, UserSubscriptions, UserLocation

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'user_type', 'image'
        )

class RoadsideCalloutAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'status', 'location', 'description', 'mechanic', 'rating', 'review'
        )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RoadsideCallout, RoadsideCalloutAdmin)
admin.site.register(UserSubscriptions)
admin.site.register(UserLocation)
