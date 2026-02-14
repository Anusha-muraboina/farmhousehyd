from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def redirect_user(user):

    if user.is_superuser:
        return redirect("superadmin-dashboard")

    elif getattr(user, "farmhouse_user", False):
        return redirect("owner_dashboard")

    return redirect("home")


def login_view(request):

    if request.user.is_authenticated:
        return redirect_user(request.user)

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            messages.error(request, "Invalid credentials")
            return redirect("accounts:login")

        login(request, user)

        return redirect_user(user)

    return render(request, "accounts/login.html")


def logout_view(request):

    logout(request)

    return redirect("accounts:login")
