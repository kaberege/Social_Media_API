from .models import Message
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()  # Using the custom User model

# Serializer class for direct messages between users
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    image = serializers.ImageField(required=False)

    class Meta:
        model = Message
        fields = "__all__"
