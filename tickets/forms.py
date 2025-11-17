from django import forms
from .models import Ticket, TicketEvent

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "order_reference", "priority", "assigned_to"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = TicketEvent
        fields = ["message"]
        widgets = { "message": forms.Textarea(attrs={"rows": 3}) }