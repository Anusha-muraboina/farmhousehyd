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
    BlogSerializer ,
    PropertyrulesSerializer
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from cms.models import *
from cms.serializers import *
from cms.models import PageSEO


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
# def home_page(request):
#     return render(request, "home.html")


def home_page(request):

    seo = PageSEO.objects.filter(page="home").first()

    return render(request, "home.html", {
        "meta_title": seo.meta_title if seo else "",
        "meta_description": seo.meta_description if seo else "",
        "meta_keywords": seo.meta_keywords if seo else "",
    })

def about(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "about.html")


def contact(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "contact.html")

# def Farmhouses(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "farmhouse_list.html")

def Farmhouses(request):

    seo = PageSEO.objects.filter(page="farmhouses").first()

    return render(request, "farmhouse_list.html", {
        "meta_title": seo.meta_title if seo else "",
        "meta_description": seo.meta_description if seo else "",
        "meta_keywords": seo.meta_keywords if seo else "",
    })

# def Farmhouse_detail(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "farmhouse_detail.html")




# def Farmhouse_detail(request, slug):
#     return render(request, "farmhouse_detail.html", {"slug": slug})





def Farmhouse_detail(request,location_slug, slug):

    farmhouse = get_object_or_404(
        # Farmhouse,
        
        Farmhouse.objects.select_related("location"),
        location__slug=location_slug,
        slug=slug,
        is_active=True
    )
    location = farmhouse.location
        # ✅ Get SEO for locations page
    page_seo = PageSEO.objects.filter(page="locations").first()

    context = {
        "farmhouse": farmhouse,
        "slug": slug,   # ✅ slug added
        "location_slug": location_slug,

        # ⭐ Dynamic SEO
        # "meta_title": location.meta_title or f"{farmhouse.title} | Farmhouse Hyd",
        # "meta_description": location.meta_description or farmhouse.short_description,
        # "meta_keywords": location.meta_keywords,
        
        "meta_title": (
            location.meta_title
            or (page_seo.meta_title if page_seo else "")
            or f"{farmhouse.title} | Farmhouse Hyd"
        ),

        "meta_description": (
            location.meta_description
            or (page_seo.meta_description if page_seo else "")
            or farmhouse.short_description
        ),

        "meta_keywords": (
            location.meta_keywords
            or (page_seo.meta_keywords if page_seo else "")
        ),
    }

    return render(request, "farmhouse_detail.html", context)



# def Farmhouse_detail(request, slug):

#     farmhouse = get_object_or_404(
#         Farmhouse,
#         slug=slug,
#         is_active=True
#     )

#     return render(request, "farmhouse_detail.html", {
#         "farmhouse": farmhouse,

#         # ⭐ SEO from model
#         "meta_title": farmhouse.meta_title or farmhouse.title,
#         "meta_description": farmhouse.meta_description or farmhouse.short_description,
#         "meta_keywords": farmhouse.meta_keywords,
#     })





from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Farmhouse, Location
from .serializers import FarmhouseSerializer, LocationSerializer ,ThingstocarrySerializer
from django.db.models import Q, F

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
        ).order_by(
            F("Slot_position").asc(nulls_last=True)
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
            "locations": location_serializer.data ,

        })


# ------------------ FARMHOUSE DETAIL API ------------------


class FarmhouseDetailAPI(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, slug):
        # 🔹 Get farmhouse with all relations optimized
        farmhouse = get_object_or_404(
            Farmhouse.objects.select_related(
                "location", "payment_policy"
            ).prefetch_related(
                "images",
                "amenities",
                "facilities",
               "thingstocarry",      # ✅ ADD THIS
               "properyrules", 
            ),
            slug=slug,
            is_active=True
        )
        # 🔹 Similar farmhouses (same location)
        similar = Farmhouse.objects.filter(
            location=farmhouse.location,
            is_active=True
        ).exclude(
            id=farmhouse.id
        ).select_related(
            "location"
        ).prefetch_related(
            "images",
            "amenities",
            "facilities"
        )[:3]

        return Response({
            "farmhouse": FarmhouseSerializer(
                farmhouse, context={"request": request}
            ).data,
            "similar_farmhouses": FarmhouseSerializer(
                similar, many=True, context={"request": request}
            ).data
        })




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
        # farmhouses = Farmhouse.objects.filter(is_active=True).order_by("slot_position")
        services = Choos_Services.objects.filter(is_active = True)
        ourfacility = OurFacility.objects.filter(is_active = True)
        know_whoweare = AboutWhoWeAre.objects.filter(is_active = True)
        selected_location = request.GET.get("location")


        search = request.GET.get("search")

        # location filter
        if selected_location:
            farmhouses = farmhouses.filter(location__slug=selected_location)

        # search filter
        if search:
            
            farmhouses = farmhouses.filter(
                Q(title__icontains=search) |
                Q(location__name__icontains=search)
            )

        
        # if selected_location:
        #     farmhouses = farmhouses.filter(location__slug=selected_location)

        latest_blogs = Blog.objects.filter(
            is_published=True
        ).order_by("-published_at")[:3]

        farmhouses = farmhouses.order_by("-created_at")[:15]

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





