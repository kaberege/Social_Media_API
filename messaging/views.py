from django.shortcuts import get_object_or_404
from .serializers import MessageSerializer
from .models import Message
from django.contrib.auth import get_user_model
from rest_framework import generics, status, filters, views
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

User = get_user_model() # Using the custom User model


class ListCreateMessageView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer # ListMessageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user  # Current user requesting the data

        # Fetch sent and received messages for the user
        sent_messages = Message.objects.filter(sender=user).order_by("-created_at")  # Get messages sent by the current user
        received_messages =  Message.objects.filter(receiver=user).order_by("-created_at") # Get messages received by the current user
        
        # Serializing sent_messages & received_messages
        sent_messages_serializer = self.get_serializer(sent_messages, many=True)
        received_messages_serializer = self.get_serializer(received_messages, many=True)
        
        # Return a response with serialized data
        return Response({
            "sent_messages":sent_messages_serializer.data,
            "received_messages":received_messages_serializer.data,
            }, status=status.HTTP_200_OK)
    '''
    def get_queryset(self):
        # Fetch the messages for the authenticated user
        user = self.request.user
        return Message.objects.filter(sender=user).order_by("-created_at") | Message.objects.filter(receiver=user).order_by("-created_at") # User.objects.filter(receiver=user) 
    '''
    def perform_create(self, serializer):
        # Save the message and set sender
        receiver_id = self.request.data.get("receiver")
        receiver = get_object_or_404(User, id=receiver_id)
        if receiver == self.request.user:
            raise PermissionDenied("You cannot send message to yourself")
        serializer.save(sender=self.request.user)

class MarkMessageAsReadView(views.APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, message_id):
        user = request.user

        try:
            # Attempting to get inbox message for the user
            message = Message.objects.get(id=message_id, receiver=user)
            message.is_read = True  # Mark message as read
            message.save()

            # Return is read message when the looked message exists
            return Response({"message": "Message is marked as read"}, status=status.HTTP_200_OK)

        except Message.DoesNotExist:
            # Return not found when the message does not exist
            return Response({"message":"Message not found"}, status=status.HTTP_404_NOT_FOUND)