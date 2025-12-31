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
