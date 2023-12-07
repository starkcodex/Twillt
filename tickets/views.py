import random
import string
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateTicketForm, AssignTicketForm
from .models import Ticket


def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ticket_id:
                id = ''.join(random.choices(string.digits,k=6))
                try:
                    var.ticket_id = id
                    var.save()
                    break
                except IntegrityError:
                    continue
            messages.success(request, 'Your ticke has been submitted. A support engineer would reach out soon.')
            return redirect('customer_tickets')
        else:
            messages.warning(request, 'something went wrong. Please Try again.')
            return redirect('customer_tickets')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request, 'ticket/create_ticket.html', context)

    
def customer_tickets(request):
    tickets = Ticket.objects.filter(customer=request.user)
    context = {'tickets':tickets}
    return render(request, 'ticket/customer_tickets.html', context)


def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id = ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned_to_engineer = True
            var.save()
            messages.success(request, f'Ticket has been assigned to {var.engineer}')
            return redirect('ticket-queue')
        else:
            messages.warning(request, 'Something went wrong. Please check input')
            return redirect('assign-ticket') 
    else:
        form = AssignTicketForm()
        context = {'form': form}
        return render(request, 'ticket/assign_ticket.html', context)
    

def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    context = {'ticket':ticket}
    return render(request, 'ticket/ticket_details.html', context)


def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned_to_engineer=False)
    context = {'tickets':tickets}
    return render(request, 'ticket/ticket_queue.html', context)