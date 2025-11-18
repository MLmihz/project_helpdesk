# billing/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BillingForm
from .models import Billing
from tickets.models import Ticket

@login_required
def create_billing(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = BillingForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.ticket = ticket  # link billing to this ticket
            billing.save()
            return redirect('ticket_detail', pk=ticket.id)
    else:
        form = BillingForm()

    return render(request, 'billing/create_billing.html', {'form': form, 'ticket': ticket})


@login_required
def billing_list(request):
    billings = Billing.objects.all().select_related('ticket', 'handled_by')
    return render(request, 'billing/billing_list.html', {'billings': billings})


@login_required
def billing_detail(request, billing_id):
    billing = get_object_or_404(Billing, id=billing_id)
    return render(request, 'billing/billing_detail.html', {'billing': billing})
