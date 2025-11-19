from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm


@login_required
def ticket_home(request):
    return render(request, "tickets/ticket_home.html")


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()
            return redirect("ticket_list")
    else:
        form = TicketForm()

    return render(request, "tickets/create_ticket.html", {"form": form})


@login_required
def ticket_list(request):
    # Customers see only their tickets
    if request.user.is_authenticated and hasattr(request.user, "role") and request.user.role == "customer":
        tickets = Ticket.objects.filter(customer=request.user)
    else:
        tickets = Ticket.objects.all()

    return render(request, "tickets/ticket_list.html", {"tickets": tickets})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})
