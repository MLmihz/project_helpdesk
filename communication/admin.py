from django.contrib import admin
from .models import Ticket, Comments, Notification

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Comments)
admin.site.register(Notification)
