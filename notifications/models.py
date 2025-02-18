# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()  # Custom user model

# Model for managing notifications
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=100)  # Describes the action (e.g., "liked", "followed", "commented on")
    
    # GenericForeignKey setup
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')  # This allows notifications to point to any model
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)  # When the notification was created

    def __str__(self):
        return f'{self.actor} {self.verb} {self.target}'
