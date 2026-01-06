from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import User

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email', '')
            user.phone = request.POST.get('phone', '')
            user.save()
            
            login(request, user)
            messages.success(request, f"Registration successful. Welcome, {user.username}!")
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def user_view(request):
    if request.method == 'POST':
        # Simple update logic
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.phone = request.POST.get('phone', '')
        request.user.save()
        
        messages.success(request, "User updated successfully!")
        return redirect('user')
        
    return render(request, 'user/user_detail.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create reset link
            reset_link = request.build_absolute_uri(
                f'/password-reset-confirm/{uid}/{token}/'
            )
            
            # Send email
            subject = 'Password Reset Request'
            message = f'Click the link below to reset your password:\n\n{reset_link}\n\nIf you did not request this, please ignore this email.'
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "No user found with that email address.")
    
    return render(request, 'user/password_reset.html')

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully! Please login.")
                return redirect('login')
            else:
                for error in form.errors.values():
                    messages.error(request, error)
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'user/password_reset_confirm.html', {
            'form': form,
            'validlink': True
        })
    else:
        return render(request, 'user/password_reset_confirm.html', {
            'validlink': False
        })
