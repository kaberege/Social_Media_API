from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, UpdateProfileAPIView, UserProfileDelete, FollowUser, UnfollowUser, CustomUserProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

# Initialize a DefaultRouter, which will automatically generate URL patterns for viewsets
router = DefaultRouter()

# Register the CustomUserProfileView with the router, this will create the appropriate URLs for user_cover CRUD operations
router.register(r'cover_profile', CustomUserProfileView, basename="custom-profile")

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),  # POST /register/
    path('login/', LoginView.as_view(), name='login'),  # POST/login/
    path('profile/', UserProfileView.as_view(), name='profile'),  # GET profile
    path('profile/update/', UpdateProfileAPIView.as_view(), name='profile_update'),  # Post / Update-profile
    path('profile/delete/', UserProfileDelete.as_view(), name='profile_delete'),  # DELETE profile
    path('follow/<int:user_id>/', FollowUser.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUser.as_view(), name='unfollow_user'),
]

urlpatterns += router.urls