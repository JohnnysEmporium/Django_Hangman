from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import Event

user = None

def log_in(request):
    global user
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.success(request, 'Wrong Username or Password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def log_out(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('home')

def sign_up(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username = request.POST['username'])
                messages.success(request, 'Username already exists')
                return redirect('signup')
            except User.DoesNotExist:
                username = request.POST['username']
                user = User.objects.create_user(username, password = request.POST['password1'])
                stats = Event(name = username)
                stats.save()
                login(request, user)
                messages.success(request, 'Account created successfully')
                return redirect('home')
        else:
            messages.success(request, 'Passwords must match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
