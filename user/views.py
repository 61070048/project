from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from event.models import Ticket

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
        user, user_context = register_func(request)
        context.update(user_context)
        if user:
            return redirect('login')
    return render(request, template_name='register.html', context=context)


@login_required
def profile(request):
    user = request.user
    tickets = user.ticket_set.all()
    if request.method == 'POST':
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.save()
    context = {
        'user': user,
        'tickets': tickets,
    }
    return render(request, template_name='profile.html', context=context)


def register_func(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    context = {'email':email,
        'username':username,
        'fname':fname,
        'lname':lname
    }
    if password == password2:
        user = User.objects.create_user(username, email, password)
        user.first_name = fname
        user.last_name = lname
        user.save()
        return user, context
    return None, context