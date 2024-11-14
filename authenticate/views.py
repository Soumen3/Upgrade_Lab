from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_signup(request):
    context ={}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully')
            return redirect('user_login')

    context['form']= RegisterForm()
    return render(request, 'authenticate/user_registration.html', context)

def user_login(request):
    context ={}
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'User logged in successfully')
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        
    context['form']= LoginForm()
    return render(request, 'authenticate/user_login.html', context)

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'User logged out successfully')
    return redirect('user_login')