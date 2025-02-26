from django.urls import path
from .views import ListCreateMessageView, MarkMessageAsReadView

urlpatterns = [
    path("messages/", ListCreateMessageView.as_view(), name="message-list"),
    path("messages/<int:message_id>/", MarkMessageAsReadView.as_view(), name="message-read"),
]