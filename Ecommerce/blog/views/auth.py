
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login


from blog.forms import LoginForm, RegisterForm
from blog.models import User


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'

                )

    return render(request, 'blog/auth/login.html', {'form': form})


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logout')
    return render(request, 'blog/auth/logout.html')


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            # login(request, user)
            return redirect('login')

    return render(request, 'blog/auth/register.html', {'form': form})
