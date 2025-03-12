from django.shortcuts import render, get_object_or_404
from rest_framework import status, views, generics, viewsets
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer, UserProfileUpdateSerializer, CustomUserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, CustomUserProfile
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()  # Custom user model

# Handle user registration requests
class RegisterView(views.APIView):
    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Register a user",
        operation_description="Handle user registration requests"
    )
    def post(self, request):
        # Initialize the serializer with the provided request data
        serializer = RegistrationSerializer(data=request.data)
        
        # Check if the data is valid according to the serializer's validation logic
        if serializer.is_valid():
            # Save the new user to the database if the data is valid
            serializer.save()
            
            # Return a success message with HTTP status 201 (Created)
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        # If the serializer data is invalid, return the validation errors with HTTP status 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Handle user login requests
class LoginView(views.APIView):
    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Login a user",
        operation_description="This handles user login requests and generates JWT"
    )
    def post(self, request):
        # Initialize the login serializer with the provided request data
        serializer = LoginSerializer(data=request.data)
        
        # Check if the provided login credentials are valid according to the serializer
        if serializer.is_valid():
            # Authenticate the user by checking the username and password
            user = authenticate(username=serializer.validated_data["username"], password=serializer.validated_data["password"])
            
            # If authentication is successful
            if user:
                # Generate JWT tokens for the authenticated user
                refresh = RefreshToken.for_user(user)
                
                # Return the access and refresh tokens along with a success message
                return Response({
                    "message": "user logged-in successfully", 
                    'refresh': str(refresh), 
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            
            # If authentication fails (invalid credentials)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        # If the serializer data is invalid, return the validation errors with HTTP status 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(views.APIView):
    # Restrict access to authenticated users only
    permission_classes = [IsAuthenticated]

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="User profile",
        operation_description="Get the currently authenticated user's profile"
    )
    def get(self, request):
        # Get the currently authenticated user from the request object
        user = request.user
        
        # Serialize the user data to return in the response
        serializer = UserProfileSerializer(user)
        
        # If serialization is successful, return the user data with HTTP status 200 (OK)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If there's an issue with the serializer, return the errors with HTTP status 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileAPIView(views.APIView):
    # Ensure only authenticated users can access this view
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Update user profile",
        operation_description="This updates a user's profile"
    )
    def put(self, request):
        #print(f"Request files: {request.FILES}")
        # Get the current authenticated user instance (the one making the request)
        instance = request.user

        # Initialize the serializer with the current user instance, the new data from the request, and 'partial=True' 
        # to allow partial updates (i.e., not all fields are required to be updated)
        serializer = UserProfileUpdateSerializer(instance, data=request.data, partial=True)

        # Check if the serializer is valid after receiving the data
        if serializer.is_valid():
            # Save the updated user profile instance to the database
            serializer.save()

            # Return the updated user data with HTTP status 200 (OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If the serializer is invalid (data is incorrect or incomplete), return the validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDelete(views.APIView):
    # Ensure only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Delete user profile",
        operation_description="This deletes a user's profile"
    )
    def delete(self, request):
        # Get the current authenticated user instance (the one making the request)
        instance = request.user
        
        # Delete the user account from the database
        instance.delete()

        # Return a success message indicating the account was deleted, with HTTP status 204 (No Content)
        return Response({"Message": "Account was deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class FollowUser(views.APIView):
    permission_classes = [IsAuthenticated]

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Follow a user",
        operation_description="This follows a user"
    )
    def post(self, request, user_id):
        # Get the user to follow or return 404 if not found
        user_to_follow = get_object_or_404(User, id=user_id)

        # Prevent users from following themselves
        if request.user == user_to_follow:
            return Response({"message": "sorry, you cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user is already following the user
        if user_to_follow in request.user.following.all():
            return Response({"message": "sorry, you've already followed this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the user to the following list
        request.user.following.add(user_to_follow)
        
         # Create a notification for the user being followed
        notification = Notification(
            recipient=user_to_follow,  # The user being followed
            actor=request.user,        # The user who is following
            verb='followed you',       # Verb explaining the action
            # Use ContentType to link the notification to the User model
            target_content_type=ContentType.objects.get_for_model(User),  # The content type for User model
            target_object_id=user_to_follow.id,  # The specific user being followed
        )
        notification.save()

        return Response({"message": "user followed successfully."}, status=status.HTTP_200_OK)

class UnfollowUser(views.APIView):
    permission_classes = [IsAuthenticated]
    
    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Unfollow a user",
        operation_description="This unfollows a user"
    )
    def post(self, request, user_id):
        # Get the user to unfollow or return 404 if not found
        user_to_unfollow = get_object_or_404(User, id=user_id)

        # Prevent users from unfollowing themselves
        if request.user == user_to_unfollow:
            return Response({"message": "sorry, you cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is in the following list
        if user_to_unfollow not in request.user.following.all():
            return Response({"message": "sorry, this user is not in your following list."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user from the following list
        request.user.following.remove(user_to_unfollow)

        return Response({"message": "user unfollowed successfully."}, status=status.HTTP_200_OK)

class CustomUserProfileView(viewsets.ModelViewSet):
    queryset = CustomUserProfile.objects.all()
    serializer_class =  CustomUserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = CustomUserProfile.objects.filter(user=self.request.user)
        return user

    def perform_create(self, serializer):
         # Check if the user already has a profile
        if CustomUserProfile.objects.filter(user=self.request.user).exists():
            raise PermissionDenied("You already have a profile. You cannot create multiple profiles.")

        # Set the current user as the custom profile owner
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Checking if the user is the owner of the custom profile before updating
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You can only update your profile cover")
        serializer.save()

    def perform_destroy(self, instance):
        # Checking if the user is the owner of the custom profile before deleting
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You can only delete your profile cover")
        instance.delete()

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Retrieve a list of custom user profiles",
        operation_description="Get a list of custom profiles for the currently authenticated user."
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of custom user profiles for the authenticated user.
        """
        return super().list(request, *args, **kwargs)

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Create a new custom user profile",
        operation_description="Create a custom user profile. A user can only have one profile."
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new custom user profile for the authenticated user.
        Only one profile is allowed per user.
        """
        return super().create(request, *args, **kwargs)

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Retrieve a specific custom user profile",
        operation_description="Get details of a specific custom user profile."
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the details of a specific custom user profile.
        """
        return super().retrieve(request, *args, **kwargs)

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Update an existing custom user profile",
        operation_description="Update an existing custom user profile. Only the profile owner can update it."
    )
    def update(self, request, *args, **kwargs):
        """
        Update the custom user profile. Only the profile owner can update it.
        """
        return super().update(request, *args, **kwargs)

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Partially update an existing custom user profile",
        operation_description="Partially update an existing custom user profile. Only the profile owner can update it."
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update the custom user profile. Only the profile owner can update it.
        """
        return super().partia_update(request, *args, **kwargs)

    # Apply swagger documentation
    @swagger_auto_schema(
        operation_summary="Delete a custom user profile",
        operation_description="Delete a custom user profile. Only the profile owner can delete it."
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete the custom user profile. Only the profile owner can delete it.
        """
        return super().destroy(request, *args, **kwargs)

