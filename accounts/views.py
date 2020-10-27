from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html', locals())


def my_profile(request):
    return render(request, 'accounts/profile.html', locals())


def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.INFO, '註冊成功')
                # messages.get_messages(request)
                return redirect('home')
            else:
                messages.add_message(request, messages.INFO, '註冊失敗')

    return render(request, 'accounts/register.html', locals())


def sign_in(request):
    # err_msg = ''
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO, '登入成功')
            return redirect('home')
        else:
            messages.add_message(request, messages.INFO, '登入失敗')

    return render(request, 'accounts/login.html', locals())


def log_out(request):
    logout(request)
    return redirect('home')
