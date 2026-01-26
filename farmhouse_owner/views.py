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


def owner_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.farmhouse_user:
            login(request, user)
            return redirect("owner_dashboard")
        else:
            messages.error(request, "Invalid credentials or not a farmhouse owner")

    return render(request, "farmhouse_admin/login.html")


@login_required
def owner_dashboard(request):
    if not request.user.farmhouse_user:
        return redirect("owner_login")

    farmhouses = Farmhouse.objects.filter(user=request.user)

    return render(request, "farmhouse_admin/dashboard.html", {
        "farmhouses": farmhouses
    })


def owner_logout(request):
    logout(request)
    return redirect("owner_login")

