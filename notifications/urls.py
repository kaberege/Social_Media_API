from django.urls import path
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('list/', NotificationListView.as_view(), name='notification-list'),  # URL route for fetching the list of notifications
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),   # The 'pk' (primary key) is used to identify the specific notification
    path('<int:pk>/unread/', MarkNotificationReadView.as_view(), name='mark-notification-unread'),  # The 'pk' (primary key) is used to identify the notification to mark as unread
]
