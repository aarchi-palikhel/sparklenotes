from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm
from .models import UserProfile

@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, '✨ Welcome to SparkleNotes! Your account has been created.')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'💖 Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, '❌ Invalid username or password!')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    messages.success(request, '👋 You have been logged out. See you soon!')
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    completed_todos = request.user.todos.filter(completed=True).count()
    
    context = {
        'user_profile': user_profile,
        'completed_todos': completed_todos,
    }
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='accounts:login')
def profile_edit(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            messages.success(request, '✨ Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })
    
    context = {
        'form': form,
        'user_profile': user_profile
    }
    return render(request, 'accounts/profile_edit.html', context)
