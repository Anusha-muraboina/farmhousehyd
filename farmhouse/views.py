from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.db.models import Q
from blogs.models import Blog
# Create your views here.
# views.py
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import AssignedUserPermission
from .models import Banner, Location, Farmhouse
from blogs.models import *
from .serializers import (
    BannerSerializer,
    LocationSerializer,
    FarmhouseSerializer,
    BlogSerializer
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from cms.models import *
from cms.serializers import *

# def home(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "home.html")

# def home(request):
#     banners = Banner.objects.filter(is_active=True).order_by('Slot_position')
#     locations = Location.objects.filter(is_active=True)

#     farmhouses = Farmhouse.objects.filter(is_active=True)

#     # 🔥 get slug, not name
#     selected_location = request.GET.get('location')

#     if selected_location:
#         farmhouses = farmhouses.filter(location__slug=selected_location)

#     latest_blogs = Blog.objects.filter(
#         is_published=True
#     ).order_by('-published_at')[:3]

#     # 🔥 limit to 3 ONLY for home page
#     farmhouses = farmhouses.order_by('-created_at')[:3]

#     return render(request, "home.html", {
#         "farmhouses": farmhouses,
#         "locations": locations,
#         "banners": banners,
#         "latest_blogs": latest_blogs,
#         "selected_location": selected_location,  # ✅ IMPORTANT
#     })

# views.py
def home_page(request):
    return render(request, "home.html")



def about(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "about.html")


def contact(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "contact.html")

def Farmhouses(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "farmhouse_list.html")
# def Farmhouse_detail(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "farmhouse_detail.html")
def Farmhouse_detail(request, slug):
    return render(request, "farmhouse_detail.html", {"slug": slug})

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Farmhouse, Location
from .serializers import FarmhouseSerializer, LocationSerializer


# ------------------ FARMHOUSE LIST API ------------------
class FarmhouseListAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        # farmhouses = Farmhouse.objects.filter(
        #     is_active=True
        # ).select_related("location").prefetch_related(
        #     "images", "amenities"
        # )
        
        farmhouses = Farmhouse.objects.filter(
            is_active=True
        ).select_related("location","payment_policy").prefetch_related(
            "images", "amenities"
        )

        # 🔍 Search
        search = request.GET.get("search")
        if search:
            farmhouses = farmhouses.filter(
                Q(title__icontains=search) |
                Q(location__name__icontains=search) |
                Q(short_description__icontains=search) |
                Q(description__icontains=search)
            )

        # 📍 Location filter
        location = request.GET.get("location")
        if location:
            farmhouses = farmhouses.filter(location__slug=location)

        # 💰 Price sort
        sort = request.GET.get("sort")
        if sort == "low_to_high":
            farmhouses = farmhouses.order_by("price_per_day")
        elif sort == "high_to_low":
            farmhouses = farmhouses.order_by("-price_per_day")

        serializer = FarmhouseSerializer(
            farmhouses, many=True, context={"request": request}
        )
        
        

        locations = Location.objects.filter(is_active=True)
        location_serializer = LocationSerializer(locations, many=True)

        return Response({
            "farmhouses": serializer.data,
            "locations": location_serializer.data
        })


# ------------------ FARMHOUSE DETAIL API ------------------
class FarmhouseDetailAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, slug):
        farmhouse = get_object_or_404(
            Farmhouse.objects.prefetch_related(
                "images", "amenities"
            ),
            slug=slug,
            is_active=True
        )

        similar = Farmhouse.objects.filter(
            location=farmhouse.location,
            is_active=True
        ).exclude(id=farmhouse.id)[:3]

        return Response({
            "farmhouse": FarmhouseSerializer(
                farmhouse, context={"request": request}
            ).data,
            "similar_farmhouses": FarmhouseSerializer(
                similar, many=True, context={"request": request}
            ).data
        })


# def Farmhouses(request):
#     # farmhouses = Farmhouse.objects.filter(is_active=True)
#     farmhouses = Farmhouse.objects.filter(is_active=True).select_related('location').prefetch_related('images')

#     locations = Location.objects.filter(is_active=True)

#     # Search Logic Improved
#     search_query = request.GET.get('search')
#     if search_query:
#         farmhouses = farmhouses.filter(
#             Q(title__icontains=search_query) | 
#             Q(location__name__icontains=search_query) |
#             Q(short_description__icontains=search_query) |
#             Q(description__icontains=search_query)
#         )

#     # Location Filter (Dropdown)
#     location_param = request.GET.get('location')
#     if location_param and location_param != 'All Locations':
#         farmhouses = farmhouses.filter(location__name=location_param)

#     # Price Sorting
#     sort_param = request.GET.get('sort')
#     if sort_param == 'low_to_high':
#         farmhouses = farmhouses.order_by('price_per_day')
#     elif sort_param == 'high_to_low':
#         farmhouses = farmhouses.order_by('-price_per_day')

#     # Prepare location list with selected status for template
#     location_list = []
#     for loc in locations:
#         location_list.append({
#             'name': loc.name,
#             'selected': loc.name == location_param
#         })

#     context = {
#         'farmhouses': farmhouses,
#         'locations': location_list,
#         'current_location': location_param,
#         'is_low_to_high': sort_param == 'low_to_high',
#         'is_high_to_low': sort_param == 'high_to_low',
#     }
#     return render(request, "farmhouse_list.html", context)


# def Farmhouse_detail(request, slug):
#     farmhouse = get_object_or_404(Farmhouse, slug=slug)
    
#     # Get similar farmhouses in the same location
#     similar_farmhouses = Farmhouse.objects.filter(
#         location=farmhouse.location, 
#         is_active=True
#     ).exclude(id=farmhouse.id)[:3]
    
#     # If not enough in same location, get some featured ones
#     if similar_farmhouses.count() < 2:
#         additional = Farmhouse.objects.filter(is_active=True).exclude(id=farmhouse.id).exclude(id__in=[f.id for f in similar_farmhouses])[:2]
#         similar_farmhouses = list(similar_farmhouses) + list(additional)

#     context = {
#         'farmhouse': farmhouse,
#         'similar_farmhouses': similar_farmhouses[:3]
#     }
#     return render(request , "farmhouse_detail.html", context)



# def Login(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "authpages/login.html")


# def Register(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "authpages/register.html")


# def PasswordResetView(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "authpages/forgot_password.html")


def BlogListing(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "blog_listing.html")


def BlogDetail(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "blog_detailpage.html")



class HomeAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        banners = Banner.objects.filter(is_active=True).order_by("Slot_position")
        locations = Location.objects.filter(is_active=True)
        farmhouses = Farmhouse.objects.filter(is_active=True)
        services = Choos_Services.objects.filter(is_active = True)
        ourfacility = OurFacility.objects.filter(is_active = True)
        know_whoweare = AboutWhoWeAre.objects.filter(is_active = True)
        selected_location = request.GET.get("location")

        if selected_location:
            farmhouses = farmhouses.filter(location__slug=selected_location)

        latest_blogs = Blog.objects.filter(
            is_published=True
        ).order_by("-published_at")[:3]

        farmhouses = farmhouses.order_by("-created_at")[:3]

        return Response({
            "banners": BannerSerializer(banners, many=True , context={"request": request}).data,
            "locations": LocationSerializer(locations, many=True).data,
            "farmhouses": FarmhouseSerializer(farmhouses, many=True , context={"request": request}).data,
            "services" : ChooseServicesSerializer(services ,many=True , context={"request": request}).data,
            "ourfacility" : OurFacilitySerializer(ourfacility ,many= True , context={"request": request}).data,
            "know_whoweare" : AboutWhoWeAreSerializer(know_whoweare,many = True , context={"request": request}).data,
            "latest_blogs": BlogSerializer(latest_blogs, many=True , context={"request": request}).data,
            "selected_location": selected_location
        })
        
        


class AboutAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        aboutsections = AboutSection.objects.filter(is_active=True)
        aboutwhoweare = WhoWeAre.objects.filter(is_active=True).order_by("Slot_position")
        travel_blogs = Blog.objects.filter(
            is_published=True
        ).order_by("-published_at")[:3]
        return Response({
            "banners": AboutSectionSerializer(
                aboutsections,
                many=True,
                context={"request": request}   # ✅ THIS IS THE FIX
            ).data,
            "travel_blogs": BlogSerializer(travel_blogs, many=True , context={"request": request}).data,
            "aboutwhoweare": WhoWeAreSerializer(
                aboutwhoweare,
                many=True,
                context={"request": request}
            ).data,
        })

        

        
# =======================================




