from django.shortcuts import render
from django.http import HttpResponse


from django.db import transaction
from decimal import Decimal
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmhouse.models import Farmhouse
from django.shortcuts import render, redirect, get_object_or_404


from django.contrib.auth import get_user_model
from accounts.views import *
User = get_user_model()

def owner_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if not getattr(request.user, "farmhouse_user", False):
            return redirect_user(request.user)

        return view_func(request, *args, **kwargs)

    return wrapper


# def redirect_user(user):

#     if user.is_superuser:
#         return redirect("superadmin-dashboard")

#     elif user.farmhouse_user:
#         return redirect("owner_dashboard")

#     else:
#         return redirect("home")   # fallback

# def login_view(request):

#     if request.user.is_authenticated:
#         return redirect_user(request.user)

#     if request.method == "POST":

#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         user = authenticate(request, email=email, password=password)

#         if not user:
#             messages.error(request, "Invalid email or password")
#             return redirect("login")

#         login(request, user)

#         # ⭐ AUTO REDIRECT
#         return redirect_user(user)

#     return render(request, "superadmin/login.html")

# def owner_login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # authenticate using EMAIL
#         user = authenticate(
#             request,
#             email=email,
#             password=password
#         )

#         if user is None:
#             messages.error(request, "Invalid email or password")
#             return redirect("owner_login")

#         # ✅ ONLY FARMHOUSE OWNER
#         if not user.farmhouse_user:
#             messages.error(request, "You are not authorized as a farmhouse owner")
#             return redirect("owner_login")

#         login(request, user)
#         return redirect("owner_dashboard")

#     return render(request, "farmhouse_admin/login.html")


def owner_logout(request):
    logout(request)
    return redirect("owner_login")



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from functools import wraps
def owner_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.farmhouse_user:
            return HttpResponseForbidden("Owner only.")

        return view_func(request, *args, **kwargs)

    return wrapper


from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
import json

@owner_required
def owner_dashboard(request):

    today = timezone.now().date()

    farmhouses = Farmhouse.objects.filter(user=request.user)

    bookings = Booking.objects.filter(
        farmhouse__in=farmhouses
    )

    ##################################################
    # ---------- BOOKING STATS ----------
    ##################################################

    stats = {

        "today_bookings":
        bookings.filter(check_in=today).count(),

        "tomorrow_bookings":
        bookings.filter(check_in=today + timedelta(days=1)).count(),

        "weekly_bookings":
        bookings.filter(check_in__gte=today - timedelta(days=7)).count(),

        "monthly_bookings":
        bookings.filter(check_in__month=today.month).count(),

        "yearly_bookings":
        bookings.filter(check_in__year=today.year).count(),

        "farmhouses":
        farmhouses.count(),
    }


    ##################################################
    # ---------- REVENUE ----------
    ##################################################

    def revenue_filter(days=None, months=None, year=False):

        qs = bookings.filter(payment_status="paid")

        if days:
            qs = qs.filter(created_at__gte=today - timedelta(days=days))

        if months:
            qs = qs.filter(
                created_at__gte=today - timedelta(days=30*months)
            )

        if year:
            qs = qs.filter(created_at__year=today.year)

        return qs.aggregate(
            total=Sum("total_amount")
        )["total"] or 0


    revenue = {

        "weekly": revenue_filter(days=7),

        "monthly": revenue_filter(days=30),

        "six_months": revenue_filter(months=6),

        "yearly": revenue_filter(year=True),
    }


    ##################################################
    # ---------- NET PROFIT ----------
    ##################################################

    avg_commission = farmhouses.aggregate(
        avg=Sum("commission_percentage")
    )["avg"] or 0

    if farmhouses.exists():
        avg_commission = avg_commission / farmhouses.count()

    yearly_net = revenue["yearly"] - (
        revenue["yearly"] * avg_commission / 100
    )


    ##################################################
    # ---------- CHART (LAST 7 DAYS BOOKINGS) ----------
    ##################################################

    last7 = bookings.filter(
        created_at__gte=today - timedelta(days=6)
    ).annotate(
        day=TruncDay("created_at")
    ).values("day").annotate(
        count=Count("id")
    ).order_by("day")


    labels = [
        d["day"].strftime("%d %b")
        for d in last7
    ]

    data = [d["count"] for d in last7]


    ##################################################
    # ---------- RECENT ----------
    ##################################################

    recent_bookings = bookings.select_related(
        "farmhouse"
    ).order_by("-created_at")[:5]


    recent_messages = ContactMessage.objects.filter(
        farmhouse__in=farmhouses
    ).order_by("-created_at")[:5]


    return render(
        request,
        "farmhouse_admin/dashboard.html",
        {
            "stats": stats,
            "revenue": revenue,
            "yearly_net": yearly_net,
            "recent_bookings": recent_bookings,
            "recent_messages": recent_messages,
            "chart_labels": json.dumps(labels),
            "chart_data": json.dumps(data),
        }
    )

from django.contrib.auth.decorators import login_required
from farmhouse.models import Farmhouse


@owner_required
def owner_farmhouses(request):

    # farmhouses = Farmhouse.objects.filter(
    #     user=request.user   # 🔥 KEY LINE
    # )
    farmhouses_qs = Farmhouse.objects.filter(
        user=request.user
    ).order_by("-id")

    paginator = Paginator(farmhouses_qs, 10)

    page = request.GET.get("page")

    farmhouses = paginator.get_page(page)

    return render(
        request,
        "farmhouse_admin/farmhouse.html",
        {"farmhouses": farmhouses}
    )
    
# @owner_required
# def add_farmhouse(request):

#     if request.method == "POST":

#         form = FarmhouseForm(request.POST)
#         pricing_form = FarmhousePricingForm(request.POST)
#         if form.is_valid() and pricing_form.is_valid():
   
#             farmhouse = form.save(commit=False)

#             farmhouse.user = request.user   # 🔥 AUTO OWNER

#             farmhouse.save()
#             form.save_m2m()

#             return redirect("owner_farmhouses")

#     else:
#         form = FarmhouseForm()

#     return render(request, "farmhouse_admin/farmhouse_form.html", {
#         "form": form
#     })

# @owner_required
# def edit_farmhouse(request, id):

#     farmhouse = get_object_or_404(
#         Farmhouse,
#         id=id,
#         user=request.user   # 🔥 SECURITY FILTER
#     )

#     form = FarmhouseForm(
#         request.POST or None,
#         instance=farmhouse
#     )

#     if form.is_valid():
#         form.save()
#         return redirect("owner_farmhouses")

#     return render(request, "farmhouse_admin/farmhouse_form.html", {
#         "form": form
#     })



@owner_required
def add_farmhouse(request):

    if request.method == "POST":

        # form = FarmhouseForm(request.POST)
        form = FarmhouseForm(request.POST, request.FILES)
        pricing_form = FarmhousePricingForm(request.POST)


        ############################################
        # 🔥 CHECK FARMHOUSE LIMIT
        ############################################
        user = request.user

        if user.farmhouse_user:
            current_count = Farmhouse.objects.filter(user=user).count()
            limit = user.farmhouse_limit or 0

            if current_count >= limit:
                messages.error(
                    request,
                    f"You can only add {limit} farmhouses."
                )

                return redirect("owner_farmhouses")



        if form.is_valid() and pricing_form.is_valid():

            farmhouse = form.save(commit=False)
            farmhouse.user = request.user   # owner
            farmhouse.save()

            form.save_m2m()

            # SAVE PRICING
            pricing = pricing_form.save(commit=False)
            pricing.farmhouse = farmhouse
            pricing.save()

            # SAVE MULTIPLE IMAGES
            images = request.FILES.getlist("gallery_images")

            for i, img in enumerate(images):
                FarmhouseImage.objects.create(
                    farmhouse=farmhouse,
                    image=img,
                    is_primary=(i == 0)
                )

            return redirect("owner_farmhouses")
        
        else:
            print("FORM ERRORS:", form.errors)
            print("PRICING ERRORS:", pricing_form.errors)

    else:
        form = FarmhouseForm()
        pricing_form = FarmhousePricingForm()

    return render(
        request,
        "farmhouse_admin/farmhouse_form.html",
        {
            "form": form,
            "pricing_form": pricing_form
        }
    )
@owner_required
def edit_farmhouse(request, id):

    farmhouse = get_object_or_404(
        Farmhouse,
        id=id,
        user=request.user
    )
    
    pricing, _ = FarmhousePricing.objects.get_or_create(
        farmhouse=farmhouse
    )

    if request.method == "POST":

        # form = FarmhouseForm(request.POST, instance=farmhouse)
        form = FarmhouseForm(request.POST, request.FILES, instance=farmhouse)
        pricing_form = FarmhousePricingForm(request.POST, instance=pricing)

        if form.is_valid() and pricing_form.is_valid():

            form.save()
            pricing_form.save()

            # ADD NEW IMAGES
            images = request.FILES.getlist("gallery_images")

            for img in images:
                FarmhouseImage.objects.create(
                    farmhouse=farmhouse,
                    image=img
                )

            return redirect("owner_farmhouses")

    else:

        form = FarmhouseForm(instance=farmhouse)
        pricing_form = FarmhousePricingForm(instance=pricing)

    return render(
        request,
        "farmhouse_admin/farmhouse_form.html",
        {
            "form": form,
            "pricing_form": pricing_form,
            "farmhouse": farmhouse
        }
    )
    
@owner_required
def delete_farmhouse(request, id):

    farmhouse = get_object_or_404(
        Farmhouse,
        id=id,
        user=request.user
    )

    farmhouse.delete()

    return redirect("owner_farmhouses")




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from booking.models import Booking
from farmhouse.models import Farmhouse
from django.core.paginator import Paginator
from django.db.models import Q


from django.contrib.auth.decorators import login_required
from booking.models import Booking
from django.core.paginator import Paginator
from farmhouse.models import Farmhouse

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from farmhouse.models import Farmhouse
from booking.models import Booking


from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render

from farmhouse.models import Farmhouse
from booking.models import Booking


@owner_required
def owner_booking_list(request):

    ###################################
    # OWNER FARMHOUSES
    ###################################
    farmhouses = Farmhouse.objects.filter(user=request.user)
    
    ###################################
    # BASE QUERY
    ###################################
    bookings = Booking.objects.filter(
        # farmhouse__in=farmhouses
         farmhouse__user=request.user 
    ).select_related("farmhouse").order_by("-created_at")
  ###################################
    # 🔢 BOOKING COUNTS (FOR TOP CARDS)
    ###################################
    pending_count = bookings.filter(status="pending").count()

    confirmed_count = bookings.filter(status="confirmed").count()

    cancelled_count = bookings.filter(status="cancelled").count()

    paid_count = bookings.filter(payment_status="paid").count()

    ###################################
    # SEARCH FILTER
    ###################################
    search = request.GET.get("search")

    if search:
        bookings = bookings.filter(
            Q(guest_name__icontains=search) |
            Q(guest_email__icontains=search) |
            Q(booking_id__icontains=search)
        )

    ###################################
    # BOOKING STATUS FILTER
    ###################################
    status = request.GET.get("status")

    if status:
        bookings = bookings.filter(status=status)

    ###################################
    # ✅ PAYMENT STATUS FILTER (NEW)
    ###################################
    payment_status = request.GET.get("payment_status")

    if payment_status:
        bookings = bookings.filter(payment_status=payment_status)

    ###################################
    # PAGINATION
    ###################################
    paginator = Paginator(bookings, 10)
    page = request.GET.get("page")
    bookings = paginator.get_page(page)

    return render(
        request,
        "farmhouse_admin/bookings/list.html",
        {
            "bookings": bookings,
            
              # top cards
            "pending_count": pending_count,
            "confirmed_count": confirmed_count,
            "cancelled_count": cancelled_count,
            "paid_count": paid_count,
        }
    )

@owner_required
def owner_booking_detail(request, pk):

    booking = get_object_or_404(
        Booking.objects.select_related("farmhouse"),
        pk=pk,
        farmhouse__user=request.user   # 🔥 SECURITY LINE
    )

    if request.method == "POST":

        booking.status = request.POST.get("status")
        booking.payment_status = request.POST.get("payment_status")
        booking.save()

        messages.success(request, "Booking updated successfully!")

        return redirect("owner_booking_detail", pk=pk)

    return render(
        request,
        "farmhouse_admin/bookings/details.html",
        {"booking": booking}
    )












from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from .serializers import *
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def owner_booking_list_api(request):

    ###################################
    # BASE QUERY
    ###################################
    # bookings = Booking.objects.filter(
    #     farmhouse__user=request.user
    # ).select_related("farmhouse").order_by("-created_at")
    
    
    ###################################
    # BASE QUERY (ONLY VIVAAN FARMHOUSE)
    ###################################
    bookings = Booking.objects.filter(
        # farmhouse__user=request.user,
        farmhouse__slug="vivaan-farmhouse"   # 👈 ADD HERE
    ).select_related("farmhouse").order_by("-created_at")
    
    
    ###################################
    # 🔢 COUNTS (TOP CARDS)
    ###################################
    pending_count = bookings.filter(status="pending").count()
    confirmed_count = bookings.filter(status="confirmed").count()
    cancelled_count = bookings.filter(status="cancelled").count()
    paid_count = bookings.filter(payment_status="paid").count()

    ###################################
    # SEARCH
    ###################################
    search = request.GET.get("search")
    if search:
        bookings = bookings.filter(
            Q(guest_name__icontains=search) |
            Q(guest_email__icontains=search) |
            Q(booking_id__icontains=search)
        )

    ###################################
    # STATUS FILTER
    ###################################
    status = request.GET.get("status")
    if status:
        bookings = bookings.filter(status=status)

    ###################################
    # PAYMENT FILTER
    ###################################
    payment_status = request.GET.get("payment_status")
    if payment_status:
        bookings = bookings.filter(payment_status=payment_status)

    ###################################
    # PAGINATION
    ###################################
    page = int(request.GET.get("page", 1))
    paginator = Paginator(bookings, 10)
    page_obj = paginator.get_page(page)

    serializer = BookingSerializer(page_obj, many=True)

    return Response({
        "results": serializer.data,

        "pagination": {
            "current_page": page,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
        },

        "counts": {
            "pending": pending_count,
            "confirmed": confirmed_count,
            "cancelled": cancelled_count,
            "paid": paid_count,
        }
    })





@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def owner_booking_detail_api(request, pk):

    booking = get_object_or_404(
        Booking.objects.select_related("farmhouse"),
        pk=pk,
        # farmhouse__user=request.user
    )

    ###################################
    # UPDATE
    ###################################
    if request.method == "POST":
        booking.status = request.data.get("status", booking.status)
        booking.payment_status = request.data.get("payment_status", booking.payment_status)
        booking.save()

        return Response({
            "message": "Booking updated successfully"
        })

    ###################################
    # GET DETAIL
    ###################################
    serializer = BookingSerializer(booking)

    return Response(serializer.data)









from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from farmhouse.models import Farmhouse
from contact.models import ContactMessage


@owner_required
def owner_contact_list(request):

    # Owner farmhouses
    farmhouses = Farmhouse.objects.filter(user=request.user)
    
    # Messages only for owner farmhouses
    messages_qs = ContactMessage.objects.filter(
        farmhouse__in=farmhouses
    ).select_related("farmhouse").order_by("-created_at")

    # 🔍 SEARCH
    search = request.GET.get("search")
    if search:
        messages_qs = messages_qs.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        )

    # Pagination
    paginator = Paginator(messages_qs, 10)
    page = request.GET.get("page")
    messages_qs = paginator.get_page(page)

    return render(
        request,
        "farmhouse_admin/messages/list.html",
        {
            "messages": messages_qs,
        }
    )



@owner_required
def owner_contact_detail(request, pk):

    message = get_object_or_404(
        ContactMessage.objects.select_related("farmhouse"),
        pk=pk,
        farmhouse__user=request.user   #  SECURITY
    )

    return render(
        request,
        "farmhouse_admin/messages/detail.html",
        {"message": message}
    )



# coupon


@owner_required
def owner_coupon_list(request):

    farmhouses = Farmhouse.objects.filter(user=request.user)

    coupons = Coupon.objects.filter(
        farmhouse__in=farmhouses
    ).select_related("farmhouse")


    # SEARCH
    search = request.GET.get("search")

    if search:
        coupons = coupons.filter(
            Q(title__icontains=search) |
            Q(code__icontains=search)
        )

    paginator = Paginator(coupons, 10)
    page = request.GET.get("page")
    coupons = paginator.get_page(page)

    return render(
        request,
        "farmhouse_admin/coupons/list.html",
        {
            "coupons": coupons
        }
    )


@owner_required
def owner_coupon_create(request):

    farmhouse = Farmhouse.objects.filter(
        user=request.user
    ).first()

    if not farmhouse:
        messages.error(request, "Create a farmhouse first.")
        return redirect("owner_farmhouses")

    if request.method == "POST":

        form = OwnerCouponForm(request.POST)

        if form.is_valid():

            coupon = form.save(commit=False)
            coupon.farmhouse = farmhouse
            coupon.save()

            messages.success(
                request,
                "Coupon created successfully!"
            )

            return redirect("owner_coupon_list")

    else:
        form = OwnerCouponForm()

    return render(
        request,
        "farmhouse_admin/coupons/form.html",
        {"form": form}
    )


@owner_required
def owner_coupon_update(request, pk):

    coupon = get_object_or_404(
        Coupon,
        pk=pk,
        farmhouse__user=request.user
    )

    if request.method == "POST":

        form = OwnerCouponForm(
            request.POST,
            instance=coupon
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Coupon updated!"
            )

            return redirect("owner_coupon_list")

    else:
        form = OwnerCouponForm(instance=coupon)

    return render(
        request,
        "farmhouse_admin/coupons/form.html",
        {"form": form}
    )


@owner_required
def owner_coupon_delete(request, pk):

    coupon = get_object_or_404(
        Coupon,
        pk=pk,
        farmhouse__user=request.user
    )

    coupon.delete()

    messages.success(
        request,
        "Coupon deleted!"
    )

    return redirect("owner_coupon_list")


# blocked


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from booking.models import BlockedDate
from django.shortcuts import redirect
from django.contrib import messages
from farmhouse_owner.forms import BlockedDateForm

# @owner_required
# def owner_blocked_dates_list(request):

#     blocked = BlockedDate.objects.select_related("farmhouse")\
#         .filter(farmhouse__user=request.user)\
#         .order_by("-created_at")
#     return render(
#         request,
#         "farmhouse_admin/blocked/list.html",
#         {"blocked": blocked}
#     )












@owner_required
def owner_blocked_dates_list(request):

    today = timezone.now().date()

    ########################################
    # BASE QUERY
    ########################################

    blocked_qs = BlockedDate.objects.select_related("farmhouse")\
        .filter(farmhouse__user=request.user)\
        .order_by("-created_at")


    ########################################
    # STATS FOR TOP CARDS
    ########################################

    total_blocks = blocked_qs.count()

    active_blocks = blocked_qs.filter(
        start_date__lte=today,
        end_date__gte=today
    ).count()

    upcoming_blocks = blocked_qs.filter(
        start_date__gt=today
    ).count()

    expired_blocks = blocked_qs.filter(
        end_date__lt=today
    ).count()


    ########################################
    # PAGINATION
    ########################################

    paginator = Paginator(blocked_qs, 10)

    page = request.GET.get("page")

    blocked = paginator.get_page(page)


    ########################################
    # RENDER
    ########################################

    return render(
        request,
        "farmhouse_admin/blocked/list.html",
        {
            "blocked": blocked,
            "total_blocks": total_blocks,
            "active_blocks": active_blocks,
            "upcoming_blocks": upcoming_blocks,
            "expired_blocks": expired_blocks,
        }
    )

from django.http import JsonResponse


from django.http import JsonResponse
from booking.models import BlockedDate, Booking
from datetime import timedelta

from django.http import JsonResponse
from booking.models import BlockedDate, Booking
# def owner_blocked_ranges(request):
#     farmhouse_id = request.GET.get("farmhouse")

#     if not farmhouse_id:
#         return JsonResponse([], safe=False)

#     blocked_ranges = []

#     blocks = BlockedDate.objects.filter(
#         farmhouse_id=farmhouse_id,
#         farmhouse__user=request.user
#     )

#     for b in blocks:
#         blocked_ranges.append({
#             "from": b.start_date.strftime("%Y-%m-%d"),
#             "to": b.end_date.strftime("%Y-%m-%d")   # checkout date
#         })

#     bookings = Booking.objects.filter(
#         farmhouse_id=farmhouse_id,
#         status__in=["pending","confirmed"]
#     )

#     for booking in bookings:
#         blocked_ranges.append({
#             "from": booking.check_in.strftime("%Y-%m-%d"),
#             "to": booking.check_out.strftime("%Y-%m-%d")
#         })

#     return JsonResponse(blocked_ranges, safe=False)


def owner_blocked_ranges(request):
    farmhouse_id = request.GET.get("farmhouse")

    if not farmhouse_id:
        return JsonResponse([], safe=False)

    blocked_ranges = []

    ########################################
    # ADMIN BLOCKED
    ########################################
    blocks = BlockedDate.objects.filter(
        farmhouse_id=farmhouse_id,
        farmhouse__user=request.user
    )

    for b in blocks:
        blocked_ranges.append({
            "from": b.start_date.strftime("%Y-%m-%d"),
            "to": (b.end_date - timedelta(days=1)).strftime("%Y-%m-%d")
        })

    ########################################
    # BOOKINGS
    ########################################
    bookings = Booking.objects.filter(
        farmhouse_id=farmhouse_id,
        status__in=["pending", "confirmed"]
    )

    for booking in bookings:
        blocked_ranges.append({
            "from": booking.check_in.strftime("%Y-%m-%d"),
            "to": (booking.check_out - timedelta(days=1)).strftime("%Y-%m-%d")
        })

    return JsonResponse(blocked_ranges, safe=False)

@owner_required
def owner_blocked_dates_create(request):

    if request.method == "POST":
        form = BlockedDateForm(request.POST, user=request.user)

        if form.is_valid():
            blocked = form.save(commit=False)

            if blocked.farmhouse.user != request.user:
                messages.error(request, "Unauthorized")
                return redirect("blocked-dates")

            blocked.save()
            messages.success(request, "Dates blocked successfully!")
            return redirect("blocked-dates")

    else:
        form = BlockedDateForm(user=request.user)

    return render(
        request,
        "farmhouse_admin/blocked/form.html",
        {"form": form}
    )



@owner_required
def owner_blocked_dates_update(request, pk):

    blocked = get_object_or_404(
        BlockedDate,
        pk=pk,
        farmhouse__user=request.user
    )

    if request.method == "POST":
        form = BlockedDateForm(
            request.POST,
            instance=blocked,
            user=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Blocked dates updated!")
            return redirect("blocked-dates")

    else:
        form = BlockedDateForm(
            instance=blocked,
            user=request.user
        )

    return render(
        request,
        "farmhouse_admin/blocked/form.html",
        {"form": form}
    )





    
# @owner_required
# def owner_blocked_dates_create(request):

#     if request.method == "POST":

#         form = BlockedDateForm(request.POST)

#         # restrict farmhouse queryset
#         form.fields["farmhouse"].queryset = \
#             request.user.farmhouses.all()

#         if form.is_valid():

#             blocked = form.save(commit=False)

#             # extra safety check
#             if blocked.farmhouse.user != request.user:
#                 messages.error(request, "Unauthorized action.")
#                 return redirect("blocked-dates")

#             blocked.save()

#             messages.success(
#                 request,
#                 "Dates blocked successfully!"
#             )

#             return redirect("blocked-dates")

#     else:
#         form = BlockedDateForm()
#         form.fields["farmhouse"].queryset = \
#             request.user.farmhouses.all()

#     return render(
#         request,
#         "farmhouse_admin/blocked/form.html",
#         {"form": form}
#     )
# @owner_required
# def owner_blocked_dates_update(request, pk):

#     blocked = get_object_or_404(
#         BlockedDate,
#         pk=pk,
#         farmhouse__user=request.user
#     )

#     if request.method == "POST":
#         form = BlockedDateForm(request.POST, instance=blocked)
#         form.fields["farmhouse"].queryset = \
#             request.user.farmhouses.all()

#         if form.is_valid():
#             form.save()

#             messages.success(
#                 request,
#                 "Blocked dates updated!"
#             )

#             return redirect("blocked-dates")

#     else:
#         form = BlockedDateForm(instance=blocked)
#         form.fields["farmhouse"].queryset = \
#             request.user.farmhouses.all()

#     return render(
#         request,
#         "farmhouse_admin/blocked/form.html",
#         {"form": form}
#     )



@owner_required
def owner_blocked_dates_delete(request, pk):

    blocked = get_object_or_404(
        BlockedDate,
        pk=pk,
        farmhouse__user=request.user
    )

    blocked.delete()

    messages.success(
        request,
        "Blocked dates removed!"
    )

    return redirect("blocked-dates")
















from farmhouse_owner.forms import FarmhousePaymentPolicy

def owner_payment_policy_list(request):

    if request.user.is_superuser:
        policies = FarmhousePaymentPolicy.objects.select_related("farmhouse")
    else:
        policies = FarmhousePaymentPolicy.objects.select_related("farmhouse").filter(
            farmhouse__user=request.user
        )

    return render(request, "farmhouse_admin/payment_policy/list.html", {
        "policies": policies
    })


def owner_payment_policy_create(request):

    form = FarmhousePaymentPolicyForm(request.POST or None)

    # 🔐 Owner can select only their farmhouses
    if not request.user.is_superuser:
        form.fields["farmhouse"].queryset = Farmhouse.objects.filter(
            user=request.user
        )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Payment Policy Created Successfully")
        return redirect("payment_policy_list")

    return render(request, "farmhouse_admin/payment_policy/form.html", {
        "form": form
    })


def owner_payment_policy_update(request, pk):

    if request.user.is_superuser:
        policy = get_object_or_404(FarmhousePaymentPolicy, pk=pk)
    else:
        policy = get_object_or_404(
            FarmhousePaymentPolicy,
            pk=pk,
            farmhouse__user=request.user
        )

    form = FarmhousePaymentPolicyForm(request.POST or None, instance=policy)

    if not request.user.is_superuser:
        form.fields["farmhouse"].queryset = Farmhouse.objects.filter(
            user=request.user
        )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Payment Policy Updated Successfully")
        return redirect("payment_policy_list")

    return render(request, "farmhouse_admin/payment_policy/form.html", {
        "form": form
    })



def owner_payment_policy_delete(request, pk):

    if request.user.is_superuser:
        policy = get_object_or_404(FarmhousePaymentPolicy, pk=pk)
    else:
        policy = get_object_or_404(
            FarmhousePaymentPolicy,
            pk=pk,
            farmhouse__user=request.user
        )

    policy.delete()
    messages.success(request, "Payment Policy Deleted Successfully")

    return redirect("payment_policy_list")











@owner_required
def owner_booking_create(request):

    # if request.headers.get("x-requested-with") == "XMLHttpRequest":
    if request.method == "GET" and request.headers.get("x-requested-with") == "XMLHttpRequest":

        farmhouse_id = request.GET.get("farmhouse_id")

        if not farmhouse_id:
            return JsonResponse([], safe=False)

        bookings = Booking.objects.filter(
            farmhouse_id=farmhouse_id,
            status="confirmed"
        )

        blocked = []

        for booking in bookings:
            start_date = booking.check_in
            end_date = booking.check_out - timedelta(days=1)  # 🔥 block only nights

            if end_date >= start_date:
                blocked.append({
                    "from": start_date.strftime("%Y-%m-%d"),
                    # "to": end_date.strftime("%Y-%m-%d"),
                    "to": booking.check_out - timedelta(days=1)
                })

        return JsonResponse(blocked, safe=False)


    if request.method == "POST":

        # form = ownerBookingForm(request.POST)
        form = ownerBookingForm(request.POST, user=request.user)
        form.fields["farmhouse"].queryset = Farmhouse.objects.filter(user=request.user)
        
        
        if form.is_valid():

            ########################################
            # DO NOT SAVE YET
            ########################################
            booking = form.save(commit=False)
            booking.user = request.user 

            ########################################
            # GET PRICING
            ########################################
            farmhouse = booking.farmhouse
            pricing = farmhouse.pricing

            start = booking.check_in
            end = booking.check_out

            subtotal = Decimal("0.00")

            while start < end:

                if pricing.sale_price and pricing.sale_price > 0:
                    subtotal += pricing.sale_price

                elif start.weekday() in [5, 6]:
                    subtotal += pricing.weekend_price

                else:
                    subtotal += pricing.normal_day_price

                start += timedelta(days=1)

            ########################################
            # EXTRA GUEST
            ########################################
            subtotal += booking.extra_guest_count * pricing.extra_guest_price

            ########################################
            # COUPON
            ########################################
            # discount = Decimal("0.00")

            # if booking.coupon_applied:
            #     coupon = booking.coupon_applied

            #     if coupon.is_active and subtotal >= coupon.min_booking_amount:
            #         discount = coupon.calculate_discount(subtotal)




            # =========================
            # COUPON DISCOUNT
            # =========================
            coupon_discount = Decimal("0.00")

            if booking.coupon_applied:
                coupon = booking.coupon_applied

                if coupon.is_active and subtotal >= coupon.min_booking_amount:
                    coupon_discount = coupon.calculate_discount(subtotal)

          
            # =========================
            # ADMIN DISCOUNT (%)
            # =========================
            admin_percent = booking.admin_discount or Decimal("0.00")

            admin_discount_amount = (
                subtotal * admin_percent / Decimal("100")
            ).quantize(Decimal("0.01"))

            # =========================
            # TOTAL DISCOUNT
            # =========================
            total_discount = coupon_discount + admin_discount_amount
            # admin_discount = booking.admin_discount or Decimal("0.00")

            # =========================
            # TOTAL DISCOUNT
            # =========================
            # total_discount = coupon_discount + admin_discount

            # SAFETY CHECK
            if total_discount > subtotal:
                total_discount = subtotal


            ########################################
            # FINAL AMOUNTS
            ########################################
            booking.sub_total = subtotal
            booking.disc_price = total_discount
            booking.tax_price = Decimal("0.00")   # add GST if needed
            # booking.total_amount = subtotal - discount
            # booking.remaining_amount = booking.total_amount


            booking.total_amount = subtotal - total_discount

            # =========================
            # ADVANCE LOGIC ✅
            # =========================
            advance = booking.advance_amount or Decimal("0.00")

            # prevent overpay
            if advance > booking.total_amount:
                advance = booking.total_amount

            booking.remaining_amount = booking.total_amount - advance
            
            
            ########################################
            # PREVENT DOUBLE BOOKING
            ########################################
            overlap = Booking.objects.filter(
                farmhouse=farmhouse,
                status="confirmed",
                check_in__lt=booking.check_out,
                check_out__gt=booking.check_in
            ).exists()

            if overlap:
                messages.error(request, "Selected dates already booked.")
                return render(
                    request,
                    "superadmin/booking/form.html",
                    {"form": form}
                )

            ########################################
            # SAVE
            ########################################
            with transaction.atomic():
                booking.save()

                transaction.on_commit(
                    lambda: booking.send_booking_email("pending", request)
                )

            messages.success(request, "Booking created successfully!")
            return redirect("admin-bookings")

    else:
        form = ownerBookingForm(user=request.user)

    return render(
        request,
        "farmhouse_admin/bookings/form.html",
        {"form": form}
    )




@owner_required
def owner_booking_update(request, pk):

    booking = get_object_or_404(Booking, pk=pk , farmhouse__user=request.user)

    old_status = booking.status

    if request.method == "POST":

        form = ownerBookingForm(
            request.POST,
            instance=booking
        )

        if form.is_valid():

            booking = form.save()

            if old_status != booking.status:

                transaction.on_commit(
                    lambda: booking.send_booking_email(
                        booking.status,
                        request
                    )
                )

            messages.success(
                request,
                "Booking updated!"
            )

            return redirect("admin-bookings")

    else:
        form = ownerBookingForm(instance=booking)

    return render(
        request,
        "farmhouse_admin/bookings/form.html",
        {"form": form}
    )


@owner_required
def owner_booking_cancel(request, pk):

    booking = get_object_or_404(Booking, pk=pk , farmhouse__user=request.user)

    try:
        booking.cancel_booking(user=request.user)

        messages.success(
            request,
            "Booking cancelled successfully!"
        )

    except Exception as e:

        messages.error(request, str(e))

    return redirect("owner-bookings")





from django.http import JsonResponse
from decimal import Decimal
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
import json


@owner_required
@require_POST
def owner_calculate_booking_price(request):
    data = json.loads(request.body)
    farmhouse_id = data.get("farmhouse")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    extra_guest_count = int(data.get("extra_guest_count", 0))
    coupon_id = data.get("coupon")

    admin_discount = Decimal(str(data.get("admin_discount", 0)))
    
    advance_amount = Decimal(str(data.get("advance_amount", 0)))

    if not farmhouse_id or not check_in or not check_out:
        return JsonResponse({"total": 0})

    try:
        farmhouse = Farmhouse.objects.select_related("pricing").get(id=farmhouse_id)
        pricing = farmhouse.pricing
    except:
        return JsonResponse({"total": 0})

    start = datetime.strptime(check_in, "%Y-%m-%d")
    end = datetime.strptime(check_out, "%Y-%m-%d")

    subtotal = Decimal("0.00")

    while start < end:

        # ⭐ SALE FIRST
        if pricing.sale_price and pricing.sale_price > 0:
            subtotal += pricing.sale_price

        elif start.weekday() in [5, 6]:
            subtotal += pricing.weekend_price

        else:
            subtotal += pricing.normal_day_price

        start += timedelta(days=1)

    ###################################
    # EXTRA GUEST
    ###################################

    subtotal += extra_guest_count * pricing.extra_guest_price

    ###################################
    # COUPON
    ###################################

    # discount = Decimal("0.00")

    # if coupon_id:

    #     coupon = Coupon.objects.filter(
    #         id=coupon_id,
    #         is_active=True
    #     ).first()

    #     if coupon and subtotal >= coupon.min_booking_amount:
    #         discount = coupon.calculate_discount(subtotal)

    # total = subtotal - discount
    
        # =========================
    # COUPON
    # =========================
    coupon_discount = Decimal("0.00")

    if coupon_id:
        coupon = Coupon.objects.filter(id=coupon_id).first()
        if coupon and coupon.is_active and subtotal >= coupon.min_booking_amount:
            coupon_discount = coupon.calculate_discount(subtotal)

    # =========================
    # ADMIN DISCOUNT (%)  ✅ ALWAYS RUN
    # =========================
    admin_percent = admin_discount or Decimal("0.00")

    admin_discount_amount = (
        subtotal * admin_percent / Decimal("100")
    ).quantize(Decimal("0.01"))

    # =========================
    # TOTAL DISCOUNT ✅ ALWAYS RUN
    # =========================
    total_discount = coupon_discount + admin_discount_amount

    if total_discount > subtotal:
        total_discount = subtotal



    total = subtotal - total_discount
    # =========================
    # ADVANCE & REMAINING
    # =========================
    if advance_amount > total:
        advance_amount = total

    remaining_amount = total - advance_amount
    
    return JsonResponse({
        # "subtotal": float(subtotal),
        # "discount": float(discount),
        # "total": float(total)
        "subtotal": float(subtotal),
        "coupon_discount": float(coupon_discount),
        "admin_discount": float(admin_discount_amount),
        "admin_percent": float(admin_percent),
        "total": float(total),
    "advance_paid": float(advance_amount),
    "remaining": float(remaining_amount)
    })





from booking.models import Invoice
@owner_required
def owner_view_invoice(request, booking_id):

    booking = get_object_or_404(
        Booking.objects.select_related("farmhouse", "user"),
        booking_id=booking_id
    )

    invoice, created = Invoice.objects.get_or_create(
        booking=booking,
        defaults={"user": booking.user}
    )

    return render(
        request,
        "emails/invoice.html",
        {
            "booking": booking,
            "invoice": invoice
        }
    )
