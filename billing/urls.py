from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing_list, name='billing_list'),
    path('<int:billing_id>/', views.billing_detail, name='billing_detail'),
    path('add/<int:ticket_id>/', views.create_billing, name='create_billing'),
]
