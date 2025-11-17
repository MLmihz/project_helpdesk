from django.contrib import admin
from .models import Ticket, TicketEvent

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority", "order_reference", "created_by", "assigned_to", "created_at")
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "description", "order_reference")

@admin.register(TicketEvent)
class TicketEventAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "event_type", "author", "from_status", "to_status", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("message",)