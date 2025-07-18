from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib import messages

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, "Username Or Password is incorrect!",
                           extra_tags='alert alert-warning alert-dismissible fade show')
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                messages.error(request, 'Password did not match!',
                             extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('accounts:register')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!',
                             extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('accounts:register')
            if len(password1) < 8:
                messages.error(request, 'Password must be at least 8 characters long!',
                             extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('accounts:register')
            user = User.objects.create_user(
                username=username,
                password=password1,
            )
            messages.success(
                request, f'Thanks for registering {user.username}.', 
                extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})