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


# def home_page(request,  location=None):

#     seo = PageSEO.objects.filter(page="home").first()

#     return render(request, "home.html", {
#         "meta_title": seo.meta_title if seo else "",
#         "meta_description": seo.meta_description if seo else "",
#         "meta_keywords": seo.meta_keywords if seo else "",
#         "location": location
#     })


# from locations.models import Location
# from seo.models import PageSEO

def home_page(request, location=None):

    meta_title = ""
    meta_description = ""
    meta_keywords = ""

    # LOCATION PAGE
    if location:

        selected_location = location.replace("_", " ")

        loc = Location.objects.filter(
            meta_title__iexact=selected_location,
            is_active=True
        ).first()

        if loc:
            meta_title = loc.meta_title
            meta_description = loc.meta_description
            meta_keywords = loc.meta_keywords

    # HOMEPAGE SEO
    else:
        seo = PageSEO.objects.filter(page="home").first()

        if seo:
            meta_title = seo.meta_title
            meta_description = seo.meta_description
            meta_keywords = seo.meta_keywords

    return render(request, "home.html", {
        "meta_title": meta_title,
        "meta_description": meta_description,
        "meta_keywords": meta_keywords,
        "location": location
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

# def Farmhouses(request):

#     seo = PageSEO.objects.filter(page="farmhouses").first()

#     return render(request, "farmhouse_list.html", {
#         "meta_title": seo.meta_title if seo else "",
#         "meta_description": seo.meta_description if seo else "",
#         "meta_keywords": seo.meta_keywords if seo else "",
#     })



def Farmhouses(request, location=None):

    location_meta = None
    location_obj = None

    if location:
        selected_location = location.replace("_", " ")

        location_obj = Location.objects.filter(
            meta_title__iexact=selected_location,
            is_active=True
        ).first()

        if location_obj:
            location_meta = {
                "meta_title": location_obj.meta_title,
                "meta_description": location_obj.meta_description,
                "meta_keywords": location_obj.meta_keywords
            }

    seo = PageSEO.objects.filter(page="farmhouses").first()

    return render(request, "farmhouse_list.html", {
        "meta_title": location_meta["meta_title"] if location_meta else (seo.meta_title if seo else ""),
        "meta_description": location_meta["meta_description"] if location_meta else (seo.meta_description if seo else ""),
        "meta_keywords": location_meta["meta_keywords"] if location_meta else (seo.meta_keywords if seo else ""),
        "current_location": location_obj.name if location_obj else None
    })
# def Farmhouse_detail(request):
#     # return HttpResponse("Hello, this is Blog Page")
#     return render(request , "farmhouse_detail.html")




# def Farmhouse_detail(request, slug):
#     return render(request, "farmhouse_detail.html", {"slug": slug})



def Farmhouse_detail(request, location_slug, slug):

    farmhouse = get_object_or_404(
        Farmhouse.objects.select_related("location"),
        location__slug=location_slug,
        slug=slug,
        is_active=True
    )
    


    context = {
        "farmhouse": farmhouse,
        "slug": slug,
        "location_slug": location_slug,

        # ✅ USE FARMHOUSE SEO (NOT LOCATION)
        "meta_title": farmhouse.meta_title or f"{farmhouse.title} | Farmhouse Hyd",

        "meta_description": farmhouse.meta_description or farmhouse.short_description,

        "meta_keywords": farmhouse.meta_keywords,
    }

    return render(request, "farmhouse_detail.html", context)

# def Farmhouse_detail(request,location_slug, slug):

#     farmhouse = get_object_or_404(
#         # Farmhouse,
        
#         Farmhouse.objects.select_related("location"),
#         location__slug=location_slug,
#         slug=slug,
#         is_active=True
#     )
#     location = farmhouse.location
#         # ✅ Get SEO for locations page
#     # page_seo = PageSEO.objects.filter(page="locations").first()

#     context = {
#         "farmhouse": farmhouse,
#         "slug": slug,   # ✅ slug added
#         "location_slug": location_slug,

#         # ⭐ Dynamic SEO
#         "meta_title": location.meta_title or f"{farmhouse.title} | Farmhouse Hyd",
#         "meta_description": location.meta_description or farmhouse.short_description,
#         "meta_keywords": location.meta_keywords,
        
#         "meta_title": (
#             location.meta_title
#             # or (page_seo.meta_title if page_seo else "")
#             or f"{farmhouse.title} | Farmhouse Hyd"
#         ),

#         "meta_description": (
#             location.meta_description
#             # or (page_seo.meta_description if page_seo else "")
#             or farmhouse.short_description
#         ),

#         "meta_keywords": (
#             location.meta_keywords
#             # or (page_seo.meta_keywords if page_seo else "")
#         ),
#     }

#     return render(request, "farmhouse_detail.html", context)



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
from django.db.models import Prefetch
from .models import Farmhouse, Location
from .serializers import FarmhouseSerializer, LocationSerializer ,ThingstocarrySerializer
from django.db.models import Q, F
from django.core.paginator import Paginator
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
            # "images",
                Prefetch(
        "images",
        queryset=FarmhouseImage.objects.order_by("-is_primary")  # ✅ KEY FIX
    ),
            
            
            "amenities"
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
        # if location:
        #     farmhouses = farmhouses.filter(location__slug=location)
        popup = None   # ✅ ADD
        if location:
            # convert URL format to meta title
            selected_location = location.replace("_", " ")

            location_obj = Location.objects.filter(
                meta_title__iexact=selected_location,
                is_active=True
            ).first()

            if location_obj:
                farmhouses = farmhouses.filter(location=location_obj)
                                # ✅ LOCATION BASED POPUP
                popup = HomePopup.objects.filter(
                    location=location_obj,
                    is_active=True
                ).first()

        # 💰 Price sort
        sort = request.GET.get("sort")
        if sort == "low_to_high":
            farmhouses = farmhouses.order_by("price_per_day")
        elif sort == "high_to_low":
            farmhouses = farmhouses.order_by("-price_per_day")


                # ⭐ PAGINATION
        page = int(request.GET.get("page", 1))
        paginator = Paginator(farmhouses, 9)

        page_obj = paginator.get_page(page)



        serializer = FarmhouseSerializer(
             page_obj.object_list,
            many=True, context={"request": request}
        )
        
        

        locations = Location.objects.filter(is_active=True)
        location_serializer = LocationSerializer(locations, many=True)
        
        return Response({
            "farmhouses": serializer.data,
            "locations": location_serializer.data ,
            "has_next": page_obj.has_next(),
            "page": page ,
                # ✅ ADD THIS
            "popup": HomePopupSerializer(
                popup, context={"request": request}
            ).data if popup else None
        })


# ------------------ FARMHOUSE DETAIL API -----------------------------------


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
               "ratings__user"
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
        #  ---------------- POPUP LOGIC ----------------

        popup = None

        # 1️ Farmhouse-specific popup (HIGH PRIORITY)
        popup = HomePopup.objects.filter(
            farmhouse=farmhouse,
            is_active=True
        ).first()

        # 2️ Location-based popup (FALLBACK)
        if not popup:
            popup = HomePopup.objects.filter(
                location=farmhouse.location,
                is_active=True
            ).first()
        return Response({
            "farmhouse": FarmhouseSerializer(
                farmhouse, context={"request": request}
            ).data,
            "similar_farmhouses": FarmhouseSerializer(
                similar, many=True, context={"request": request}
            ).data,
                 # ✅ SEND POPUP
            "popup": HomePopupSerializer(
                popup, context={"request": request}
            ).data if popup else None
        })




def BlogListing(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "blog_listing.html")


def BlogDetail(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "blog_detailpage.html")





from django.db.models import Q
from django.db.models import Q
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny

from .serializers import HomePopupSerializer
# from django.db.models import Q
# from django.core.cache import cache
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions import AllowAny

class HomeAPIView(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    # def get(self, request, location=None):

    #     search = request.GET.get("search")

    #     selected_location = None

    #     # convert URL underscore → space
    #     if location:
    #         selected_location = location.replace("_", " ")
    def get(self, request):
        location = request.GET.get("location")
        search = request.GET.get("search")

        selected_location = None

        if location:
            selected_location = location.replace("_", " ")

        cache_key = f"home_page_data_{selected_location}_{search}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        banners = Banner.objects.filter(is_active=True).order_by("Slot_position")
        locations = Location.objects.filter(is_active=True)
        farmhouses = Farmhouse.objects.filter(is_active=True)

        services = Choos_Services.objects.filter(is_active=True)
        ourfacility = OurFacility.objects.filter(is_active=True)
        know_whoweare = AboutWhoWeAre.objects.filter(is_active=True)

        popup = HomePopup.objects.filter(is_active=True).first()

        location_meta = None

        # ✅ LOCATION FILTER
        if selected_location:

            location_obj = Location.objects.filter(
                meta_title__iexact=selected_location,
                is_active=True
            ).first()

            if location_obj:

                farmhouses = farmhouses.filter(location=location_obj)

                location_meta = {
                    "meta_title": location_obj.meta_title,
                    "meta_description": location_obj.meta_description,
                    "meta_keywords": location_obj.meta_keywords
                }

        # ✅ SEARCH FILTER
        if search:
            farmhouses = farmhouses.filter(
                Q(title__icontains=search) |
                Q(location__name__icontains=search) |
                        Q(short_description__icontains=search) |
        Q(description__icontains=search)
            )


        latest_blogs = Blog.objects.filter(
            is_published=True
        ).order_by("-published_at")[:3]

        # farmhouses = farmhouses.order_by("-created_at")[:6]
        
        
        
                # ✅ LIMITED (FOR UI GRID)
        limited_farmhouses = farmhouses.order_by("-created_at")[:6]

        # ✅ FULL DATA (FOR SEARCH DROPDOWN)
        all_farmhouses = Farmhouse.objects.filter(is_active=True)

        # if not search:
        #    farmhouses = farmhouses[:6]
        
        # ✅ LIMIT ONLY WHEN NO SEARCH & NO LOCATION
        # if not search and not selected_location:
        #     farmhouses = farmhouses[:6]

        data = {

            "popup": HomePopupSerializer(
                popup,
                context={"request": request}
            ).data if popup else None,

            "location_meta": location_meta,

            "banners": BannerSerializer(
                banners, many=True, context={"request": request}
            ).data,

            "locations": LocationSerializer(
                locations, many=True
            ).data,

            # "farmhouses": FarmhouseSerializer(
            #     farmhouses, many=True, context={"request": request}
            # ).data,
            
            
             # ✅ FOR GRID (LIMITED)
            "farmhouses": FarmhouseSerializer(
                limited_farmhouses, many=True, context={"request": request}
            ).data,

            # ✅ FOR SEARCH DROPDOWN (FULL)
            "all_farmhouses": FarmhouseSerializer(
                all_farmhouses, many=True, context={"request": request}
            ).data,

            "services": ChooseServicesSerializer(
                services, many=True, context={"request": request}
            ).data,

            "ourfacility": OurFacilitySerializer(
                ourfacility, many=True, context={"request": request}
            ).data,

            "know_whoweare": AboutWhoWeAreSerializer(
                know_whoweare, many=True, context={"request": request}
            ).data,

            "latest_blogs": BlogSerializer(
                latest_blogs, many=True, context={"request": request}
            ).data,
            
        }

        cache.set(cache_key, data, 60 * 5)

        return Response(data)

    
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





# class HomeAPIView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         banners = Banner.objects.filter(is_active=True).order_by("Slot_position")
#         locations = Location.objects.filter(is_active=True)
#         farmhouses = Farmhouse.objects.filter(is_active=True)
#         # farmhouses = Farmhouse.objects.filter(is_active=True).order_by("slot_position")
#         services = Choos_Services.objects.filter(is_active = True)
#         ourfacility = OurFacility.objects.filter(is_active = True)
#         know_whoweare = AboutWhoWeAre.objects.filter(is_active = True)
#         selected_location = request.GET.get("location")


#         search = request.GET.get("search")

#         # location filter
#         if selected_location:
#             farmhouses = farmhouses.filter(location__slug=selected_location)



#                # create unique cache key based on filters
#         cache_key = f"home_page_data_{selected_location}_{search}"

#         cached_data = cache.get(cache_key)

#         if cached_data:
#             return Response(cached_data)

#         # search filter
#         if search:
            
#             farmhouses = farmhouses.filter(
#                 Q(title__icontains=search) |
#                 Q(location__name__icontains=search)
#             )

#         # if selected_location:
#         #     farmhouses = farmhouses.filter(location__slug=selected_location)

#         latest_blogs = Blog.objects.filter(
#             is_published=True
#         ).order_by("-published_at")[:3]

#         farmhouses = farmhouses.order_by("-created_at")[:9]

#         return Response({
#             "banners": BannerSerializer(banners, many=True , context={"request": request}).data,
#             "locations": LocationSerializer(locations, many=True).data,
#             "farmhouses": FarmhouseSerializer(farmhouses, many=True , context={"request": request}).data,
#             "services" : ChooseServicesSerializer(services ,many=True , context={"request": request}).data,
#             "ourfacility" : OurFacilitySerializer(ourfacility ,many= True , context={"request": request}).data,
#             "know_whoweare" : AboutWhoWeAreSerializer(know_whoweare,many = True , context={"request": request}).data,
#             "latest_blogs": BlogSerializer(latest_blogs, many=True , context={"request": request}).data,
#             "selected_location": selected_location
#         })
        
        

# from django.core.cache import cache
# from farmhouse.serializers import HomePopupSerializer

# class HomeAPIView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [AllowAny]

#     def get(self, request):


#         selected_location = request.GET.get("location")
#         search = request.GET.get("search")

#         # create unique cache key based on filters
#         cache_key = f"home_page_data_{selected_location}_{search}"

#         cached_data = cache.get(cache_key)

#         if cached_data:
#             return Response(cached_data)

#         banners = Banner.objects.filter(is_active=True).order_by("Slot_position")
#         locations = Location.objects.filter(is_active=True)
#         farmhouses = Farmhouse.objects.filter(is_active=True)
#         services = Choos_Services.objects.filter(is_active=True)
#         ourfacility = OurFacility.objects.filter(is_active=True)
#         know_whoweare = AboutWhoWeAre.objects.filter(is_active=True)
        
#         popup = HomePopup.objects.filter(is_active=True).first()
        
#         # location filter
#         if selected_location:
#             farmhouses = farmhouses.filter(location__slug=selected_location)

#         # search filter
#         if search:
#             farmhouses = farmhouses.filter(
#                 Q(title__icontains=search) |
#                 Q(location__name__icontains=search)
#             )

#         latest_blogs = Blog.objects.filter(
#             is_published=True
#         ).order_by("-published_at")[:3]

#         farmhouses = farmhouses.order_by("-created_at")[:6]

#         data = {
#            "popup": HomePopupSerializer(
#                 popup,
#                 context={"request": request}
#             ).data if popup else None,

#             "banners": BannerSerializer(
#                 banners, many=True, context={"request": request}
#             ).data,

#             "locations": LocationSerializer(
#                 locations, many=True
#             ).data,

#             "farmhouses": FarmhouseSerializer(
#                 farmhouses, many=True, context={"request": request}
#             ).data,

#             "services": ChooseServicesSerializer(
#                 services, many=True, context={"request": request}
#             ).data,

#             "ourfacility": OurFacilitySerializer(
#                 ourfacility, many=True, context={"request": request}
#             ).data,

#             "know_whoweare": AboutWhoWeAreSerializer(
#                 know_whoweare, many=True, context={"request": request}
#             ).data,

#             "latest_blogs": BlogSerializer(
#                 latest_blogs, many=True, context={"request": request}
#             ).data,

#             "selected_location": selected_location
#         }


#         # store in redis cache (5 minutes)
#         cache.set(cache_key, data, 60 * 5)

#         return Response(data)




















from django.http import JsonResponse
from datetime import timedelta
from booking.models import Booking, BlockedDate

########################################
# OWNER CALENDAR
########################################
# @owner_required
def owner_farmhouse_calendar(request, pk):

    farmhouse = get_object_or_404(
        Farmhouse,
        pk=pk,
        # user=request.user
    )

    return render(
        request,
        "calendar.html",
        {"farmhouse": farmhouse}
    )


########################################
# PUBLIC CALENDAR (NO LOGIN)
########################################
def public_calendar(request, slug):

    farmhouse = get_object_or_404(
        Farmhouse,
        slug=slug,
        is_active=True
    )

    return render(
        request,
        "calendar.html",   # ✅ separate template
        {"farmhouse": farmhouse}
    )


from django.http import JsonResponse
from datetime import timedelta, date
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import timedelta, date
from django.shortcuts import get_object_or_404
import calendar
from datetime import date

def get_calendar_data(request, slug):

    farmhouse = get_object_or_404(Farmhouse, slug=slug)

    result = []

    # ✅ GET MONTH FROM FRONTEND
    year = int(request.GET.get("year", date.today().year))
    month = int(request.GET.get("month", date.today().month))

    # ✅ FULL MONTH RANGE
    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    current = start_date

    #################################
    # LOOP FULL MONTH
    #################################
    while current <= end_date:

        offer = farmhouse.offers.filter(
            start_date__lte=current,
            end_date__gte=current
        ).first()

        price = farmhouse.get_price_by_date(current)

        result.append({
            "date": current.strftime("%Y-%m-%d"),
            "price": float(price) if price else None,
            "is_offer": bool(offer),
            "type": "available"
        })

        current += timedelta(days=1)

    #################################
    # BOOKINGS
    #################################
    # bookings = Booking.objects.filter(
    #     farmhouse=farmhouse,
    #     status__in="confirmed"   )
    
    bookings = Booking.objects.filter(
    farmhouse=farmhouse,
    status="confirmed"
    )

    for booking in bookings:
        start = booking.check_in
        end = booking.check_out - timedelta(days=1)

        while start <= end:
            result.append({
                "date": start.strftime("%Y-%m-%d"),
                "type": "booked"
            })
            start += timedelta(days=1)

    #################################
    # BLOCKED
    #################################
    blocks = BlockedDate.objects.filter(farmhouse=farmhouse)

    for b in blocks:
        start = b.start_date
        end = b.end_date - timedelta(days=1)

        while start <= end:
            result.append({
                "date": start.strftime("%Y-%m-%d"),
                "type": "blocked"
            })
            start += timedelta(days=1)

    return JsonResponse(result, safe=False)