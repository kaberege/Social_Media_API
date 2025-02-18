from django.shortcuts import render, get_object_or_404
from rest_framework import filters, views, viewsets, status, generics
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like
from django.contrib.auth import authenticate, get_user_model
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework
from rest_framework.response import Response
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()  # Custom user model

# Pagination class to handle post pagination
class PostPagination(PageNumberPagination):
    page_size = 10  # Number of posts per page

# Viewset for managing posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'created_at']
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'title', 'created_at']
    ordering = ['id']
    
    def perform_create(self, serializer):
         # Automatically set the author of the post to the current logged-in user
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Check if the user is the author before updating
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You can only update your own posts!")
        serializer.save()

    def perform_destroy(self, instance):
        # Check if the user is the author before deleting
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own posts!")
        instance.delete()

    @swagger_auto_schema(
        operation_summary="Retrieve a list of posts",
        operation_description="Get a paginated list of posts with optional filtering, searching, and ordering."
    )
    def list(self, request, *args, **kwargs):
        """
        Get a paginated list of posts with optional filtering, searching, and ordering.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new post",
        operation_description="Create a new post. The author is automatically set to the logged-in user."
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new post.
        The author field is set to the logged-in user automatically.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific post by its ID",
        operation_description="Get details of a single post by its ID."
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Get details of a single post by its ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update an existing post",
        operation_description="Update an existing post. Only the post's author can update it."
    )
    def update(self, request, *args, **kwargs):
        """
        Update an existing post. Only the post's author can update it.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a post",
        operation_description="Delete a post. Only the post's author can delete it."
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a post. Only the post's author can delete it.
        """
        return super().destroy(request, *args, **kwargs)

# View for displaying a user's feed (posts from followed users)
class PostFeed(generics.ListAPIView):
    #queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'created_at']
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'title', 'created_at']
    ordering = ["-created_at"]

    def get_queryset(self):
        # Get posts from users that the current user is following
        following_users = self.request.user.following.all()
        feed = Post.objects.filter(author__in=following_users).order_by('-created_at')
        return feed

     # Adding Swagger documentation
    @swagger_auto_schema(
        operation_summary="Retrieve posts from followed users",
        operation_description="This endpoint returns a list of posts from users that the authenticated user is following, ordered by creation date. You can filter by post title, content, and creation date. You can also search posts by title or content."
    )
    def get(self, request, *args, **kwargs):
        """
        Get the posts from followed users for the current authenticated user.
        """
        return super().get(request, *args, **kwargs)

# Viewset for managing comments on posts
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination
     # Enable Filtering, Searching, and Ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Define the filter fields
    filterset_fields = ['content', 'created_at']
    search_fields = ['content']
    ordering_fields = ['id', 'content', 'created_at']
    ordering = ['id']  # Default ordering by id

    def perform_create(self, serializer):
        # Save the comment with the logged-in user as the author
        comment = serializer.save(author=self.request.user)

        # Create a notification for the post author (notify them about the new comment)
        post = comment.post  # comment is linked to a post
        if post.author != self.request.user:
            # Notify the post author about the new comment
            Notification.objects.create(
                recipient=post.author,  # The user who owns the post
                actor=self.request.user,  # The user who made the comment
                verb='commented on your post',  # Action description
                target_content_type=ContentType.objects.get_for_model(Post),  # Content type of the post
                target_object_id=post.id  # The ID of the post
            )

    def perform_update(self, serializer):
        # Check if the user is the author before updating
        if self.get_object().author != self.request.user:
            raise PermissionDenied("You can only update your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        # Check if the user is the author before deleting
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()
    
    @swagger_auto_schema(
        operation_summary="Retrieve a list of comments",
        operation_description="Get a paginated list of comments on posts, with optional filtering, searching, and ordering."
    )
    def list(self, request, *args, **kwargs):
        """
        Get a paginated list of comments with optional filtering, searching, and ordering.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new comment",
        operation_description="Create a new comment on a post. The author is automatically set to the logged-in user, and a notification is sent to the post author."
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new comment. The author is automatically set to the logged-in user.
        A notification is sent to the post author about the new comment.
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific comment by its ID",
        operation_description="Get details of a specific comment by its ID."
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Get details of a specific comment by its ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update an existing comment",
        operation_description="Update an existing comment. Only the comment's author can update it."
    )
    def update(self, request, *args, **kwargs):
        """
        Update an existing comment. Only the comment's author can update it.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a comment",
        operation_description="Delete a comment. Only the comment's author can delete it."
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a comment. Only the comment's author can delete it.
        """
        return super().destroy(request, *args, **kwargs)

# View for liking a post
class LikePostView(views.APIView):
    @swagger_auto_schema(
        operation_summary="Like a post",
        operation_description="View for liking a post"
    )
    def post(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, pk=post_id)

        # Check if the user is trying to like their own post
        if post.author == user:
            return Response({'detail': 'You cannot like your own post.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create a Like object
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if not created:
            return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
         
         # Create a notification for the post's author when a post is liked
        notification = Notification(
            recipient=post.author,  # The author of the post
            actor=user,             # The user who liked the post
            verb='liked your post', # Verb explaining the action
            # ContentType to link the notification to the Post model
            target_content_type=ContentType.objects.get_for_model(Post),  # The content type of the Post model
            target_object_id=post.id,  # The specific post that was liked
        )
        notification.save()
        
        return Response({'detail': 'You liked this post.'}, status=status.HTTP_201_CREATED)

# View for unliking a post
class UnlikePostView(views.APIView):
    @swagger_auto_schema(
        operation_summary="Unlike a post",
        operation_description="View for unliking a post"
    )
    def delete(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, pk=post_id)

        # Check if the user is trying to unlike their own post
        if post.author == user:
            return Response({'detail': 'You cannot unlike your own post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Try to get the Like object, or return a 404 error if it doesn't exist
        try:
            like = Like.objects.get(user=user, post=post)  # This will raise Like.DoesNotExist if no like exists
            like.delete()  # If found, delete the like
            return Response({'detail': 'You unliked this post.'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)
