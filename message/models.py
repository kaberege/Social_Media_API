from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # custom user model

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to="inbox_images/", null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
