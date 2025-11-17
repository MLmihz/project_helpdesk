from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import Ticket, TicketEvent
from .forms import TicketForm, CommentForm

def is_agent(user):
    return user.is_staff  # adjust later if you add roles

@login_required
def ticket_list(request):
    qs = Ticket.objects.select_related("created_by", "assigned_to")
    if not request.user.is_staff:
        qs = qs.filter(created_by=request.user)
    status_param = request.GET.get("status")
    if status_param:
        qs = qs.filter(status=status_param)
    return render(request, "tickets/list.html", { "tickets": qs })

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket.objects.select_related("created_by", "assigned_to"), pk=pk)
    if not request.user.is_staff and ticket.created_by_id != request.user.id:
        return redirect("ticket_list")
    comment_form = CommentForm()
    return render(request, "tickets/detail.html", { "ticket": ticket, "comment_form": comment_form })

@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect("ticket_detail", pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, "tickets/form.html", { "form": form, "title": "Create Ticket" })

@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not request.user.is_staff and ticket.created_by_id != request.user.id:
        return redirect("ticket_list")
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("ticket_detail", pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, "tickets/form.html", { "form": form, "title": "Update Ticket" })

@user_passes_test(is_agent)
def ticket_transition(request, pk, to_status):
    ticket = get_object_or_404(Ticket, pk=pk)
    if to_status not in {c for c, _ in Ticket.Status.choices}:
        return redirect("ticket_detail", pk=pk)
    if ticket.status != to_status:
        with transaction.atomic():
            from_status = ticket.status
            ticket.status = to_status
            ticket.save(update_fields=["status", "updated_at"])
            TicketEvent.objects.create(
                ticket=ticket,
                event_type=TicketEvent.EventType.STATUS_CHANGE,
                author=request.user,
                from_status=from_status,
                to_status=to_status,
            )
    return redirect("ticket_detail", pk=pk)

@login_required
def ticket_comment(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not request.user.is_staff and ticket.created_by_id != request.user.id:
        return redirect("ticket_list")
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            TicketEvent.objects.create(
                ticket=ticket,
                event_type=TicketEvent.EventType.COMMENT,
                author=request.user,
                message=form.cleaned_data["message"],
            )
    return redirect("ticket_detail", pk=pk)