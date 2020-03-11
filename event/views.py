from datetime import date, datetime, time
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from event.models import Category, Event, Ticket
from user.views import register_func

# Create your views here.

def payment(request, event_id):
    user = request.user
    amount = int(request.GET.get('amount') if request.GET.get('amount') else request.POST.get('amount'))
    event = Event.objects.get(pk=event_id)
    context = {
        "total_price" : event.ticket_price * amount,
        "event" : event,
        "amount" : amount,
        "email" : user.email if user.is_authenticated else '',
        "action" : "payment"
    }
    if amount > event.ticket_amount:
        return redirect('detail', event_id=event.id)
    elif request.method == 'POST':
        if not user.is_authenticated:
            user, user_context = register_func(request)
            context.update(user_context)
        if user:
            for i in range(0, amount):
                Ticket.objects.create(event_id=event.id, user_id=user.id)
                event.ticket_amount -= 1
            event.save()
            if user.is_authenticated:
                return redirect('index')
            else:
                return redirect('login')

    return render(request, template_name='payment.html', context=context)


def index(request):
    events = Event.objects.filter(event_date__gte = date.today(), ticket_amount__gt = 0).order_by('-is_popular','event_date','event_time')[:5]
    categories = Category.objects.all().order_by('name')[0:5]
    for e in events:
        e.location = e.location if len(e.location) < 60 else e.location[0:55]+"..."
    context = {
        'events':events,
        'categories': categories
    }
    return render(request, template_name='index.html', context=context)


def query_event(request):
    search =  request.GET.get('search')
    category =  request.GET.get('category')
    lookup = (Q())
    header = "All Event"
    if search:
        lookup = (Q(event_name__icontains = search))
        header = "Search for " + search
    elif category:
        lookup = (Q(category__id = category))
        header = "Category " + category
    events = Event.objects.filter(
        event_date__gte = date.today(), ticket_amount__gt = 0).filter(lookup).order_by('-is_popular','event_date','event_time')
    for e in events:
        e.location = e.location if len(e.location) < 60 else e.location[0:55]+"..."
    context = {
        'events':events,
        'header':header
    }
    return render(request, template_name='event.html', context=context)


def query_category(request):
    lookup = (Q())
    categories = Category.objects.all().order_by('name')[0:25]
    context = {
        'categories':categories,
    }
    return render(request, template_name='category.html', context=context)


def detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    context = {}
    if request.method == 'POST' and request.POST.get('amount'):
        amount = int(request.POST.get('amount'))
        if amount <= event.ticket_amount and amount > 0:
            return redirect(reverse('payment', kwargs={'event_id':event.id}) + '?amount=%d'%amount)
        context["amount"] = amount
        context["error"] = 'Ticket not enough' if amount > 0 else 'Amount must be positive number'
    context["event"] = event
    return render(request, template_name='detail.html', context=context)
