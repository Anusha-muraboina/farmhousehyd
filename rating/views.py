from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def rating(request):
    return HttpResponse("Hello, this is Blog Page")
