from django.shortcuts import render

# Create your views here.
# views.py
from django.http import HttpResponse

def home(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "home.html")


def about(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "about.html")


def contact(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "contact.html")


def destination(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "destination.html")


def Farmhouses(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "farmhouse_list.html")


def Farmhouse_detail(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "farmhouse_detail.html")


def Login(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "authpages/login.html")


def Register(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "authpages/register.html")


def PasswordResetView(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "authpages/forgot_password.html")


def BlogListing(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "blog_listing.html")


def BlogDetail(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "blog_detailpage.html")