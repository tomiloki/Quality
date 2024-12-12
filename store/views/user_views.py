# store/views/user_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from store.forms import UserRegistrationForm
from django.contrib.auth.models import User

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
    return render(request, 'store/login.html')

def user_logout(request):
    logout(request)
    return redirect('product_list')
