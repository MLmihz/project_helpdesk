from django.urls import include, path
from . import views
from django.urls import path
from .views import user_profile, register_page


app_name = 'users'

urlpatterns = [
  path('profile/', views.user_profile, name='user_profile'),
  path('register/', register_page, name='register_page'),
  path('login/', views.login_page, name='login'),
  path('logout/', views.logout_page, name='logout'),
  path('profile/', views.UserProfileView.as_view(), name='profile'),
  path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile-detail'),
  path('list/', views.user_list_page, name='list'),
  path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
  path('profile/', user_profile, name='user_profile'),
        
]