from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "is_read", "created_at", "updated_at")  # Fields to be displayed in the admin panel
    list_filter = ("sender", "is_read", "created_at", "updated_at") # Adding filters for easy searching
    search_fields = ("sender", "receiver", "is_read") # Adding search fields

admin.site.register(Message, MessageAdmin)