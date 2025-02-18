from django.contrib import admin
from .models import Notification

# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor', 'verb', 'target', 'is_read', 'timestamp')
    list_filter = ('verb', 'is_read')
    search_fields = ('verb','timestamp')


admin.site.register(Notification, NotificationAdmin)