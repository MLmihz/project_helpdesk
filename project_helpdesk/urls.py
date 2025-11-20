
from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('billing/', include('billing.urls')),  
    path('tickets/', include('tickets.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('communication/', include('communication.urls')),
    path('notifications/', lambda request: __import__('django').http.HttpResponseRedirect('/communication/notifications/')),
    path('', dashboard_home, name='home'),
    
]
