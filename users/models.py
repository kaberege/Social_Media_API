from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

# Custom manager for user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        # Ensure email is provided
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)  # Normalize email address
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Set the password
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Call create_user to handle superuser creation
        return self.create_user(username, email, password, **extra_fields)


# Custom user model extending AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False) # Email is unique and required
    bio = models.CharField(max_length=250, blank=True, null=True)  # Optional Bio field
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # Optional Profile Picture field
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)  # Many-to-many field for users to follow each other
   
    REQUIRED_FIELDS = ['email']  # Specify the fields that are required when creating a user (excluding the username)
   
    objects = CustomUserManager()  # Custom manager for handling user creation

    def __str__(self):
        return self.username

# Customized user profile with additional fields like location, website, & cover photo
class CustomUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to CustomUser model
    location = models.CharField(max_length=100, blank=True, null=True)  # Optional Location field
    website = models.URLField(max_length=200, blank=True, null=True)  # Optional Website field
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)  # Optional Cover Photo field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"