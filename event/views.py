from datetime import date, datetime, time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from event.models import Category, Event, Ticket

# Create your views here.

def my_login(request):
    context = {} 
    user = request.user         
    if user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user=user)
            return redirect('index')
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    return render(request, template_name='login.html', context=context)


def my_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    context = {'action':'register'}
    if request.method == 'POST':
        user = register_func(request, context)
        redirect('login')
    return render(request, template_name='register.html', context=context)


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
    if event.users.all().count()+amount > event.ticket_amount:
        return redirect('detail', event_id=event.id)
    elif request.method == 'POST':
        if not user.is_authenticated:
            user = register_func(request, context)
        for i in range(0, amount):
            Ticket.objects.create(event_id=event.id, user_id=user.id)
        if user.is_authenticated:
            return redirect('index')
        else:
            return redirect('login')

    return render(request, template_name='payment.html', context=context)


def index(request):
    events = Event.objects.filter(event_date__gte = date.today())[:5]
    print(date)
    print(events)
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
    if search:
        lookup = (Q(event_name__icontains = search))
    elif category:
        lookup = (Q(category__id = category))
    events = Event.objects.filter(
        event_date__gte = date.today()).filter(lookup).order_by('-is_popular','event_date','event_time')[:10]
    for e in events:
        e.location = e.location if len(e.location) < 60 else e.location[0:55]+"..."
    context = {
        'events':events,
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
    ticket = event.ticket_amount - event.users.all().count()
    if request.method == 'POST' and request.POST.get('amount'):
        amount = int(request.POST.get('amount'))
        if amount <= ticket and amount > 0:
            return redirect(reverse('payment', kwargs={'event_id':event.id}) + '?amount=%d'%amount)
        context["amount"] = amount
        context["error"] = 'Ticket not enough' if amount > 0 else 'Amount must be positive number'
    context["event"] = event
    context["ticket"] = ticket
    return render(request, template_name='detail.html', context=context)


def register_func(request, context_data):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    if password == password2:
        user = User.objects.create_user(username, email, password)
        user.first_name = fname
        user.last_name = lname
        user.save()
        return user
    context = {'email':email,
        'username':username,
        'fname':fname,
        'lname':lname
    }
    context.update(context_data)
    return render(request, template_name='%s.html'%context.action, context=context)


def create_mockUP(request):
    for i in range(13, 25):
        category = Category.objects.create(name="Test-%d"%i)
        Event.objects.create(event_name="Test-event-%d"%i, event_date=date(2020, 4, 13), event_time=time(12, 0, 0), location="Test-locate-%d"%i, ticket_price="99", ticket_amount="99", picture="photos/w_92LbIKE.PNG", category=category, is_popular=i%2==0)
    return redirect('index')
