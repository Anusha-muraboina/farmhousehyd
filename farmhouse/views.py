from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from blogs.models import Blog
# Create your views here.
# views.py
from django.http import HttpResponse

# def home(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "home.html")

def home(request):
    banners = Banner.objects.filter(is_active=True).order_by('Slot_position')
    locations = Location.objects.filter(is_active=True)

    farmhouses = Farmhouse.objects.filter(is_active=True)

    # 🔥 get slug, not name
    selected_location = request.GET.get('location')

    if selected_location:
        farmhouses = farmhouses.filter(location__slug=selected_location)

    latest_blogs = Blog.objects.filter(
        is_published=True
    ).order_by('-published_at')[:3]

    # 🔥 limit to 3 ONLY for home page
    farmhouses = farmhouses.order_by('-created_at')[:3]

    return render(request, "home.html", {
        "farmhouses": farmhouses,
        "locations": locations,
        "banners": banners,
        "latest_blogs": latest_blogs,
        "selected_location": selected_location,  # ✅ IMPORTANT
    })

# def home(request):
#     # Fetch banners
#     banners = Banner.objects.filter(is_active=True).order_by('Slot_position')
    
#     # Fetch recent active farmhouses
#     farmhouses = Farmhouse.objects.filter(is_active=True)
    
#     # Fetch all active locations to show in the banner
#     locations = Location.objects.filter(is_active=True)
    
#     location_param = request.GET.get('location')
#     if location_param and location_param != 'All Locations':
#         farmhouses = farmhouses.filter(location__name=location_param)
        
#     latest_blogs = Blog.objects.filter(is_published=True).order_by('-published_at')[:3]
    
#     farmhouses = farmhouses.order_by('-created_at')[:3]
#     return render(request, "home.html", {
#         'farmhouses': farmhouses,
#         'locations': locations,
#         'banners': banners,
#         'latest_blogs': latest_blogs
#     })

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
    # farmhouses = Farmhouse.objects.filter(is_active=True)
    farmhouses = Farmhouse.objects.filter(is_active=True).select_related('location').prefetch_related('images')

    locations = Location.objects.filter(is_active=True)

    # Search Logic Improved
    search_query = request.GET.get('search')
    if search_query:
        farmhouses = farmhouses.filter(
            Q(title__icontains=search_query) | 
            Q(location__name__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Location Filter (Dropdown)
    location_param = request.GET.get('location')
    if location_param and location_param != 'All Locations':
        farmhouses = farmhouses.filter(location__name=location_param)

    # Price Sorting
    sort_param = request.GET.get('sort')
    if sort_param == 'low_to_high':
        farmhouses = farmhouses.order_by('price_per_day')
    elif sort_param == 'high_to_low':
        farmhouses = farmhouses.order_by('-price_per_day')

    # Prepare location list with selected status for template
    location_list = []
    for loc in locations:
        location_list.append({
            'name': loc.name,
            'selected': loc.name == location_param
        })

    context = {
        'farmhouses': farmhouses,
        'locations': location_list,
        'current_location': location_param,
        'is_low_to_high': sort_param == 'low_to_high',
        'is_high_to_low': sort_param == 'high_to_low',
    }
    return render(request, "farmhouse_list.html", context)


def Farmhouse_detail(request, slug):
    farmhouse = get_object_or_404(Farmhouse, slug=slug)
    
    # Get similar farmhouses in the same location
    similar_farmhouses = Farmhouse.objects.filter(
        location=farmhouse.location, 
        is_active=True
    ).exclude(id=farmhouse.id)[:3]
    
    # If not enough in same location, get some featured ones
    if similar_farmhouses.count() < 2:
        additional = Farmhouse.objects.filter(is_active=True).exclude(id=farmhouse.id).exclude(id__in=[f.id for f in similar_farmhouses])[:2]
        similar_farmhouses = list(similar_farmhouses) + list(additional)

    context = {
        'farmhouse': farmhouse,
        'similar_farmhouses': similar_farmhouses[:3]
    }
    return render(request , "farmhouse_detail.html", context)



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