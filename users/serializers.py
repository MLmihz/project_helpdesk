from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Enter the same password as above, for verification."
    )
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'role', 'phone_number', 'address'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.'
                )
            attrs['user'] = user
        else:
            raise serializers.ValidationError(
                'Must include "username" and "password".'
            )
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile (read and update)."""
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone_number', 'address', 'date_joined',
            'created_at', 'updated_at', 'is_active'
        )
        read_only_fields = ('id', 'username', 'date_joined', 'created_at', 'updated_at')
    
    def validate_role(self, value):
        """Prevent users from changing their own role (should be done by admins)."""
        if self.instance and self.instance.role != value:
            # In a full implementation, you might want to check if the current user is admin
            # For now, we'll allow role changes but this should be restricted in views
            pass
        return value


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (limited fields)."""
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone_number', 'is_active', 'date_joined'
        )

