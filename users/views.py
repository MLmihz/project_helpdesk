from django.contrib.auth import logout

# Standard HTML logout view
def logout_page(request):
    logout(request)
    return redirect('users:login')
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return redirect('users:list')
        except User.DoesNotExist:
            pass
    return redirect('users:list')
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserListSerializer
)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_profile(request):
    return render(request, 'users/userprofile.html', {'user': request.user})

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    Allows anyone to create a new user account.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    """
    API endpoint for user login.
    Returns authentication token on successful login.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profile.
    Users can only view/edit their own profile unless they are admin.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        # Users can only access their own profile unless they are admin
        if self.request.user.is_admin:
            user_id = self.kwargs.get('pk')
            if user_id:
                try:
                    return User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return self.request.user
        return self.request.user
    
    def get_queryset(self):
        return User.objects.all()


class UserListView(generics.ListAPIView):
    """
    API endpoint for listing users.
    Admins can see all users, agents can see customers, customers can only see themselves.
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            # Admins can see all users
            return User.objects.all()
        elif user.is_agent:
            # Agents can see customers
            return User.objects.filter(role='customer')
        else:
            # Customers can only see themselves
            return User.objects.filter(id=user.id)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    """
    API endpoint for user logout.
    Deletes the authentication token.
    """
    try:
        # Delete the user's token to logout
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Error during logout'},
            status=status.HTTP_400_BAD_REQUEST
        )

from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User

def user_list_page(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def register_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/users/login/')  # Change to your login URL name if needed
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Standard HTML login view
def login_page(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:user_profile')
        else:
            error = 'Invalid username or password.'
    return render(request, 'users/login.html', {'error': error})
