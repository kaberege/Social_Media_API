from django.shortcuts import render
from rest_framework import views, generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from django_filters import rest_framework
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema

# This view handles the listing of notifications for an authenticated user
class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_read', 'timestamp']
    search_fields = ['is_read', 'timestamp']
    ordering_fields = ['is_read', 'timestamp']
    #ordering = ['id']

    def list(self, request, *args, **kwargs):
        """
        Overriding list to fetch and return unread notifications prominently at the top.
        """
        user = request.user
        
        # Fetch unread notifications first, then read notifications
        unread_notifications = Notification.objects.filter(recipient=user, is_read=False).order_by('-timestamp')
        read_notifications = Notification.objects.filter(recipient=user, is_read=True).order_by('-timestamp')

        # Serialize unread and read notifications
        unread_serializer = NotificationSerializer(unread_notifications, many=True)
        read_serializer = NotificationSerializer(read_notifications, many=True)

        # Return the response, showcasing unread notifications first
        return Response({
            'unread_notifications': unread_serializer.data,  # Unread first
            'read_notifications': read_serializer.data,      # Read after
        }, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_summary="Retrieve a list of notifications",
        operation_description="This endpoint returns a list of notifications for the authenticated user, with unread notifications listed first, followed by read notifications. Notifications are ordered by timestamp, with the most recent appearing at the top. You can filter the notifications by read/unread status."
     )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        

# View to mark a specific notification as read or unread
class MarkNotificationReadView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Mark notifications as read",
        operation_description="This marks notifications as read"
    )
    def post(self, request, pk):
        try:
            # Attempt to get the notification for the user
            notification = Notification.objects.get(id=pk, recipient=request.user)
            notification.is_read = True  # Mark as read
            notification.save()
            return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            # If notification is not found, return a 404 error
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Mark notifications as unread",
        operation_description="This marks notifications as unread"
    )
    def delete(self, request, pk):
        try:
            # Attempt to get the notification for the user
            notification = Notification.objects.get(id=pk, recipient=request.user)
            notification.is_read = False  # Mark as unread
            notification.save()
            return Response({"message": "Notification marked as unread"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            # If notification is not found, return a 404 error
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
