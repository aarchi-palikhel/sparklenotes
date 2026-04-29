import logging

logger = logging.getLogger(__name__)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm, PasswordResetRequestForm, SetNewPasswordForm
from .models import UserProfile

# Max upload size: 5 MB
MAX_AVATAR_SIZE = 5 * 1024 * 1024
ALLOWED_AVATAR_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}


# ── Helpers ────────────────────────────────────────────────────────────────────

def send_welcome_email(user, request):
    """Send a welcome email to a newly registered user."""
    subject = '✨ Welcome to SparkleNotes!'
    html_message = render_to_string('accounts/emails/welcome_email.html', {
        'user': user,
        'request': request,
    })
    plain_message = strip_tags(html_message)
    logger.debug('Attempting welcome email to %s via %s', user.email, settings.EMAIL_HOST_USER)
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.debug('Welcome email sent successfully to %s', user.email)
    except Exception as e:
        logger.error('Welcome email failed for %s: %s', user.email, e)


def send_password_reset_email(user, request):
    """Send a password reset link to the user."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = request.build_absolute_uri(
        f'/accounts/password-reset/confirm/{uid}/{token}/'
    )
    subject = '🔑 Reset Your SparkleNotes Password'
    html_message = render_to_string('accounts/emails/password_reset_email.html', {
        'user': user,
        'reset_url': reset_url,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


# ── Avatar Serve View ──────────────────────────────────────────────────────────

def avatar(request, user_id):
    """Serve a user's avatar image directly from the database."""
    profile = get_object_or_404(UserProfile, user_id=user_id)
    if profile.avatar_data is None or len(profile.avatar_data) == 0:
        from django.http import Http404
        raise Http404
    content_type = profile.avatar_content_type or 'image/jpeg'
    return HttpResponse(bytes(profile.avatar_data), content_type=content_type)


# ── Auth Views ─────────────────────────────────────────────────────────────────

@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            if user.email:
                send_welcome_email(user, request)
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
            login_input = form.cleaned_data['login'].strip()
            password = form.cleaned_data['password']

            # Try username first, then fall back to email lookup
            user = authenticate(request, username=login_input, password=password)

            if user is None:
                # Maybe they entered an email — find the username and retry
                try:
                    matched = User.objects.get(email__iexact=login_input)
                    user = authenticate(request, username=matched.username, password=password)
                except User.DoesNotExist:
                    pass

            if user is not None:
                login(request, user)
                if user.is_staff or user.is_superuser:
                    messages.success(request, f'👑 Welcome, {user.username}! Redirecting to admin panel.')
                    return redirect('admin:index')
                messages.success(request, f'💖 Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, '❌ Invalid username/email or password!')
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
            # Save User model fields directly from POST (not via ModelForm)
            request.user.first_name = request.POST.get('first_name', '').strip()
            request.user.last_name = request.POST.get('last_name', '').strip()
            new_email = request.POST.get('email', '').strip()
            if new_email:
                request.user.email = new_email
            request.user.save()

            profile = form.save(commit=False)

            # Handle avatar upload — store bytes directly in the DB
            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                content_type = avatar_file.content_type
                if content_type not in ALLOWED_AVATAR_TYPES:
                    messages.error(request, '❌ Unsupported image type. Use JPG, PNG, GIF or WebP.')
                    return render(request, 'accounts/profile_edit.html', {
                        'form': form, 'user_profile': user_profile
                    })
                if avatar_file.size > MAX_AVATAR_SIZE:
                    messages.error(request, '❌ Image too large. Maximum size is 5 MB.')
                    return render(request, 'accounts/profile_edit.html', {
                        'form': form, 'user_profile': user_profile
                    })
                profile.avatar_data = avatar_file.read()
                profile.avatar_content_type = content_type

            profile.save()
            messages.success(request, '✨ Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/profile_edit.html', context)


# ── Password Reset Views ───────────────────────────────────────────────────────

@require_http_methods(["GET", "POST"])
def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_password_reset_email(user, request)
            except User.DoesNotExist:
                pass
            return redirect('accounts:password_reset_done')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset.html', {'form': form})


def password_reset_done(request):
    return render(request, 'accounts/password_reset_done.html')


@require_http_methods(["GET", "POST"])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_valid = user is not None and default_token_generator.check_token(user, token)

    if not token_valid:
        return render(request, 'accounts/password_reset_invalid.html')

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, '🎉 Password reset successful! You can now log in.')
            return redirect('accounts:login')
    else:
        form = SetNewPasswordForm()

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})
