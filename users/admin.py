from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User  # Tells Django that this admin is for the custom User model
    
    # List display in the admin panel
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'is_active', 'bio'
    )
    
    # Fields to filter by in the admin panel
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    
    # Fields to search by in the admin panel
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Default ordering in the admin panel
    ordering = ('username',)

    # Customize the fieldsets (used for editing existing users)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'followers')}),  # Add 'bio' and 'profile_picture' fields
    )

    # Customize the add_fieldsets (used for creating new users)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'profile_picture', 'followers' )}),  # Add 'bio' and 'profile_picture' fields
    )

# Register the custom user model with the custom admin interface
admin.site.register(User, CustomUserAdmin)
