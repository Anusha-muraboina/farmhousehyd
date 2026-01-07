from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def booking(request):
    return HttpResponse("Hello, this is Blog Page")
