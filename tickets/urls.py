from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_home, name='ticket_home'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('list/', views.ticket_list, name='ticket_list'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
]
