from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, PostFeed, CommentViewset, LikePostView, UnlikePostView

# Initialize a DefaultRouter, which will automatically generate URL patterns for viewsets
router = DefaultRouter()

# Register the PostViewSet with the router, this will create the appropriate URLs for Post CRUD operations
router.register(r"posts_all", PostViewSet, basename="post-viewset-list")

# Register the CommentViewset with the router, this will create the appropriate URLs for Comment CRUD operations
router.register(r"comments_all", CommentViewset, basename="comment-viewset-list")

urlpatterns = [
    path("", include(router.urls)), # Include the automatically generated URLs for the Post and Comment viewsets
    path("feed/", PostFeed.as_view(), name="post_feed"), # URL for the PostFeed view, which shows the current user's feed of posts from followed users
    path('<int:post_id>/like/', LikePostView.as_view(), name='like_post'), # URL for liking a post, using the LikePostView, where <int:post_id> is the ID of the post being liked
    path('<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike_post'), # URL for unliking a post, using the UnlikePostView, where <int:post_id> is the ID of the post being unliked
]
