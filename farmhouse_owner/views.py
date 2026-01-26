from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def farmhouse_owner(request):
    return HttpResponse("Hello, this is farmhouse_owner Page")






from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmhouse.models import Farmhouse


from django.contrib.auth import get_user_model

User = get_user_model()

def owner_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # authenticate using EMAIL
        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("owner_login")

        # ✅ ONLY FARMHOUSE OWNER
        if not user.farmhouse_user:
            messages.error(request, "You are not authorized as a farmhouse owner")
            return redirect("owner_login")

        login(request, user)
        return redirect("owner_dashboard")

    return render(request, "farmhouse_admin/login.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("owner_login")

        if not request.user.farmhouse_user:
            return redirect("owner_login")

        return view_func(request, *args, **kwargs)
    return wrapper


@owner_required
def owner_dashboard(request):
    return render(request, "farmhouse_admin/dashboard.html")


def owner_logout(request):
    logout(request)
    return redirect("owner_login")

