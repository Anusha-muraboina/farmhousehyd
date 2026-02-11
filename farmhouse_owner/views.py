from django.shortcuts import render
from django.http import HttpResponse




from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmhouse.models import Farmhouse
from django.shortcuts import render, redirect, get_object_or_404


from django.contrib.auth import get_user_model

User = get_user_model()

def owner_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # authenticate using EMAIL
        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect("owner_login")

        # ✅ ONLY FARMHOUSE OWNER
        if not user.farmhouse_user:
            messages.error(request, "You are not authorized as a farmhouse owner")
            return redirect("owner_login")

        login(request, user)
        return redirect("owner_dashboard")

    return render(request, "farmhouse_admin/login.html")


def owner_logout(request):
    logout(request)
    return redirect("owner_login")



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("owner_login")

        if not request.user.farmhouse_user:
            return redirect("owner_login")

        return view_func(request, *args, **kwargs)
    return wrapper


from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
import json

@login_required(login_url="owner_login")
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


@login_required(login_url="owner_login")
def owner_farmhouses(request):

    farmhouses = Farmhouse.objects.filter(
        user=request.user   # 🔥 KEY LINE
    )

    return render(
        request,
        "farmhouse_admin/farmhouse.html",
        {"farmhouses": farmhouses}
    )
    
@login_required(login_url="owner_login")
def add_farmhouse(request):

    if request.method == "POST":

        form = FarmhouseForm(request.POST)

        if form.is_valid():

            farmhouse = form.save(commit=False)

            farmhouse.user = request.user   # 🔥 AUTO OWNER

            farmhouse.save()
            form.save_m2m()

            return redirect("owner_farmhouses")

    else:
        form = FarmhouseForm()

    return render(request, "farmhouse_admin/farmhouse_form.html", {
        "form": form
    })

@login_required(login_url="owner_login")
def edit_farmhouse(request, id):

    farmhouse = get_object_or_404(
        Farmhouse,
        id=id,
        user=request.user   # 🔥 SECURITY FILTER
    )

    form = FarmhouseForm(
        request.POST or None,
        instance=farmhouse
    )

    if form.is_valid():
        form.save()
        return redirect("owner_farmhouses")

    return render(request, "farmhouse_admin/farmhouse_form.html", {
        "form": form
    })

@login_required(login_url="owner_login")
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


# @login_required
# def owner_booking_list(request, farmhouse_id):

#     #########################################
#     # SECURITY 🔥 VERY IMPORTANT
#     #########################################

#     farmhouse = get_object_or_404(
#         Farmhouse,
#         id=farmhouse_id,
#         user=request.user   # ⭐ prevents hacking
#     )

#     bookings = Booking.objects.filter(
#         farmhouse=farmhouse
#     ).select_related("user").order_by("-created_at")

#     #########################################
#     # SEARCH
#     #########################################

#     search = request.GET.get("search")

#     if search:
#         bookings = bookings.filter(
#             Q(guest_name__icontains=search) |
#             Q(guest_email__icontains=search) |
#             Q(booking_id__icontains=search)
#         )

#     #########################################
#     # STATUS FILTER
#     #########################################

#     status = request.GET.get("status")

#     if status:
#         bookings = bookings.filter(status=status)

#     #########################################
#     # PAGINATION
#     #########################################

#     paginator = Paginator(bookings, 10)
#     page = request.GET.get("page")
#     bookings = paginator.get_page(page)

#     return render(
#         request,
#         "farmhouse_admin/bookings/list.html",
#         {
#             "farmhouse": farmhouse,
#             "bookings": bookings
#         }
#     )
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


@login_required
def owner_booking_list(request):

    ###################################
    # OWNER FARMHOUSES
    ###################################
    farmhouses = Farmhouse.objects.filter(user=request.user)

    ###################################
    # BASE QUERY
    ###################################
    bookings = Booking.objects.filter(
        farmhouse__in=farmhouses
    ).select_related("farmhouse").order_by("-created_at")

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
        }
    )

@login_required
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



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from farmhouse.models import Farmhouse
from contact.models import ContactMessage


@login_required
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



@login_required
def owner_contact_detail(request, pk):

    message = get_object_or_404(
        ContactMessage.objects.select_related("farmhouse"),
        pk=pk,
        farmhouse__user=request.user   # 🔥 SECURITY
    )

    return render(
        request,
        "farmhouse_admin/messages/detail.html",
        {"message": message}
    )



# coupon


@login_required
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


@login_required
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


@login_required
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


@login_required
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
