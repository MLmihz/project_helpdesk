from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name= 'comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f'Comment by {self.author.username} on {self.ticket.title}'
    
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient.username} - {self.message}'
