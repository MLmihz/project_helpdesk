
from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('billing/', include('billing.urls')),  
    path('tickets/', include('tickets.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('communication/', include('communication.urls')),
    path('', dashboard_home, name='home'),
]
