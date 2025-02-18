from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model() # Custom user

    # Serializer for user registration
class RegistrationSerializer(serializers.ModelSerializer):
     # Define fields for password and profile_picture
    password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "bio", "profile_picture"]

       # Override the create method to handle user creation logic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user # Return the created user instance
     
    # Serializer for user login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    # Serializer for viewing the user's profile
class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "profile_picture"]

    def get_profile_picture(self, obj):
        # Return URL or None if no profile picture exists
        return obj.profile_picture.url if obj.profile_picture else None

    # Serializer for updating a user's profile
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "bio", "profile_picture"]

    def update(self, instance, validated_data):
        # Handle profile_picture
        profile_picture = validated_data.pop("profile_picture", None)
        # Debugging: Print out the received profile_picture
        '''
        if profile_picture:
            print(f"Received profile_picture: {profile_picture}")
        else:
            print("No profile picture received")
        '''

        # Pop the password field from validated_data to handle separately
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        # Update the profile_picture if it's provided (set to None if no image is provided)
        if profile_picture is not None:
            instance.profile_picture = profile_picture

        # Save the instance
        instance.save()
        return instance
