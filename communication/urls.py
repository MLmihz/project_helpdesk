from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='communication_home'),
    path('comments/', views.comments_list, name='comments_list'),
    path('notifications/', views.notifications_list, name='notifications_list'),
]
