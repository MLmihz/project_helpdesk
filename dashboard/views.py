from django.shortcuts import render
from tickets.models import Ticket
from billing.models import Billing
from django.db.models import Sum

def dashboard_home(request):
    total_tickets = Ticket.objects.count()
    total_billing = Billing.objects.count()
    total_revenue = Billing.objects.filter(payment_status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    recent_tickets = Ticket.objects.order_by('-created_at')[:5]

    context = {
        'total_tickets': total_tickets,
        'total_billing': total_billing,
        'total_revenue': total_revenue,
        'recent_tickets': recent_tickets,
    }
    return render(request, 'dashboard/index.html', context)
