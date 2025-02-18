
# Social Media API - Backend Capstone Project

## Overview

A backend Social Media API built using Django and Django REST Framework (DRF). 
The API supports CRUD operations for posts, user management, and relationships between users. 
Features include post creation, user following, and a personalized feed, with JWT authentication for secure access.


## Features

- Post Management: Create, read, update, delete posts.
- Comment Management: Create, read, update, delete comments.
- User Management: Register, update, and delete user accounts.
- Follow System: Users can follow/unfollow others.
- Feed: View posts from followed users, with pagination and sorting.
- Likes & Comments: Users can like and comment on posts.
- Notifications: Users receive notifications when someone follows them, likes their post, or comments on their post.
- JWT Authentication: Secure access to endpoints via JSON Web Tokens.


## Installation

### Requirements

- asgiref==3.8.1
- Django==5.1.4
- django-filter==24.3
- djangorestframework==3.15.2
- djangorestframework-simplejwt==5.3.1
- pillow==11.0.0
- PyJWT==2.10.1
- sqlparse==0.5.3
- typing_extensions==4.12.2
- tzdata==2024.2

### Setup

1. Clone the repository:
    git clone https://github.com/kaberege2/social-media-api.git
    cd social-media-api

2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Set up the database (PostgreSQL or other DB):
    - Configure in `settings.py`.
    - Run migrations:
      python manage.py migrate

5. Create a superuser (for admin access):
    python manage.py createsuperuser

6. Run the development server:
    python manage.py runserver

## API Endpoints

### Authentication

- POST `/users/register/` - Register a new user.
- POST `/users/login/` - Login and receive JWT token.

### Post Management

- GET `/posts/posts_all/` - List user's posts.
- POST `/posts/posts_all/` - Create a new post.
- GET `/posts/posts_all/{id}/` - View a specific post.
- PUT `/posts/posts_all/{id}/` - Update a post (user's own).
- DELETE `/posts/posts_all/{id}/` - Delete a post (user's own).

### User & Follow Management

- POST `users/follow/{id}/` - Follow or unfollow a user.
- GET `users/feed/` - View posts from followed users.

### Likes and Comments
- POST `/like/{post_id}/` - Like a post.
- DELETE `/unlike/{post_id}/` - Unlike a post.
- GET `/posts/comments_all/` - List comments.
- POST `/posts/comments_all/` - Create a new comment.
- GET `/posts/comments_all/{id}/` - View a specific comment.
- PUT `/posts/comments_all/{id}/` - Update a comment (user's own).
- DELETE `/posts/comments_all/{id}/` - Delete a comment (only the comment's author can delete).

### Notifications
- GET `/notifications/list/` - Get notifications for the authenticated user (e.g., follows, likes, comments).
- POST `/notifications/{notification_id}/read/` - Mark a notification as read.
- DELETE `/notifications/{notification_id}/unread/` - Mark a notification as unread.


### JWT Token-based Authentication

- JWT token required for accessing most endpoints, provided after login.

