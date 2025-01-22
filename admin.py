from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

# Register the custom User model with the admin interface
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Customize the User admin view if necessary
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

# Register the Profile model with the admin interface
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'pincode')
