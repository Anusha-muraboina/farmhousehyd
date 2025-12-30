from django.shortcuts import render

# Create your views here.
# views.py
from django.http import HttpResponse

def blog_page(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "home.html")
