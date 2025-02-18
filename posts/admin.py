from django.contrib import admin
from .models import Post, Comment, Like

# Define the admin interface for the Post model
class PostAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of posts
    list_display = ('title', 'author', 'created_at', 'updated_at')
    # Add filters for post author and timestamps for easy searching
    list_filter = ('author', 'created_at', 'updated_at')
    # Enable search functionality for post title and content
    search_fields = ("title", "content")

# Define the admin interface for the Comment model
class CommentAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of comments
    list_display = ('post', 'author', 'created_at', 'updated_at')
    # Add filters for comment author and timestamps for easy searching
    list_filter = ('author', 'created_at', 'updated_at')
    # Enable search functionality for post, author, and content of the comment
    search_fields = ("post", 'author', "content")

# Define the admin interface for the Like model
class LikeAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view of likes
    list_display = ('user', 'post')
    # Add filters for user and post to easily filter likes
    list_filter = ('user', 'post')
    # Enable search functionality for user and post fields
    search_fields = ('user', 'post')

# Register the models with their respective admin configurations
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
