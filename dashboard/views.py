from django.shortcuts import render

def dashboard_home(request):
    return render(request, 'dashboard/dashboard_home.html')
