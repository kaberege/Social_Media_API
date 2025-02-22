from django.urls import path
from .views import ListCreateMessageView

urlpatterns = [
    path("messages/", ListCreateMessageView.as_view(), name="message-list")
]