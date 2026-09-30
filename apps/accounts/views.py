from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from .forms import RegisterForm, LoginForm, ProfileForm, AdminPasswordChangeForm

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to CerebroX AI! Now add the courses you want to study.')
            return redirect('learning:courses')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        identifier = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=identifier, password=password)
        if user is None:
            # allow logging in with email as well as username
            try:
                candidate = User.objects.get(email__iexact=identifier)
                user = authenticate(request, username=candidate.username, password=password)
            except User.DoesNotExist:
                user = None
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('admin_panel:dashboard' if user.is_admin_role else 'dashboard:home')
        messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'accounts/login.html', {'form': LoginForm()})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You've been signed out.")
    return redirect('public:landing')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = AdminPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('accounts:profile')
    else:
        form = AdminPasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})
