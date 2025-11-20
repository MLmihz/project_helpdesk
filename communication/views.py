from django.shortcuts import render
from .models import Comment, Notification

def home(request):
    comments = Comment.objects.all()
    notifications = Notification.objects.all()
    return render(request, 'communication/home.html', {
        'comments': comments,
        'notifications': notifications
    })

def comments_list(request):
    comments = Comment.objects.all()
    from .models import Ticket
    tickets = Ticket.objects.all()
    return render(request, 'communication/comments.html', {'comments': comments, 'tickets': tickets})

def notifications_list(request):
    notifications = Notification.objects.all()
    return render(request, 'communication/notifications.html', {'notifications': notifications})
