from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Custom user model

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to="inbox_images/", null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
