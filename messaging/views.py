from django.shortcuts import get_object_or_404
from .serializers import MessageSerializer
from .models import Message
from django.contrib.auth import get_user_model
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

User = get_user_model() # Using the custom User model


class ListCreateMessageView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer # ListMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Fetch the messages for the authenticated user
        user = self.request.user
        return Message.objects.filter(sender=user).order_by("-created_at") | Message.objects.filter(receiver=user).order_by("-created_at") # User.objects.filter(receiver=user) 
    
    def perform_create(self, serializer):
        # Save the message and set sender
        receiver_id = self.request.data.get("receiver")
        receiver = get_object_or_404(User, id=receiver_id)
        if receiver == self.request.user:
            raise PermissionDenied("You cannot send message to yourself")
        serializer.save(sender=self.request.user)

