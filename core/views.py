import re
from django.shortcuts import redirect, render
from .models import Profile
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate
from django.contrib import auth
User = get_user_model()
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

# Create your views here.

@login_required(login_url='signin')
def index(request):

    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.info(request, 'You are logged in')
            return redirect('/')
        else:
            messages.info(request, 'Wrong')
            return redirect('signin')
    return render(request, 'signin.html')

@login_required(login_url='signin')
def logoutPage(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def accountSettings(request):

    return render(request, 'setting.html')

