from django.shortcuts import render

# Create your views here.
# Create your views here.

from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from blogs.models import *

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
# def superadmin_required(view_func):
#     return user_passes_test(
#         lambda u: u.is_authenticated and u.is_superuser
#     )(view_func)
from django.http import HttpResponseForbidden
from functools import wraps
from django.http import HttpResponseForbidden

# def superadmin_required(view_func):

#     def wrapper(request, *args, **kwargs):

#         if not request.user.is_superuser:
#             return HttpResponseForbidden("Superadmin only.")

#         return view_func(request, *args, **kwargs)

#     return wrapper


from django.shortcuts import redirect

from accounts.views import *
def superadmin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("accounts:login")

        if not request.user.is_superuser:
            return redirect_user(request.user)

        return view_func(request, *args, **kwargs)

    return wrapper


# def superadmin_login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         user = authenticate(request, email=email, password=password)

#         if user and user.is_superuser:
#             login(request, user)
#             return redirect("superadmin-dashboard")

#         messages.error(request, "Invalid credentials or not Super Admin")

#     return render(request, "superadmin/login.html")


from farmhouse.models import Farmhouse
from django.contrib.auth import get_user_model

User = get_user_model()

# @superadmin_required
# def superadmin_dashboard(request):
#     context = {
#         "total_users": User.objects.count(),
#         "total_farmhouses": Farmhouse.objects.count(),
#         "active_farmhouses": Farmhouse.objects.filter(is_active=True).count(),
#     }
#     return render(request, "superadmin/dashboard.html", context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user.models import User
from farmhouse.models import Farmhouse
from contact.models import ContactMessage

# @login_required
# def superadmin_dashboard(request):
#     context = {
#         "total_users": User.objects.count(),
#         "total_farmhouses": Farmhouse.objects.count(),
#         "total_bookings": 0,  # add later
#         "total_messages": ContactMessage.objects.count(),

#         "recent_users": User.objects.order_by("-date_joined")[:5],
#         "recent_messages": ContactMessage.objects.order_by("-created_at")[:5],
#     }

#     return render(request, "superadmin/dashboard.html", context)




from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from booking.models import Booking
from farmhouse.models import Farmhouse

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
import json

from booking.models import Booking
from farmhouse.models import Farmhouse


@superadmin_required
def superadmin_dashboard(request):

    #########################################
    # DATE SETUP
    #########################################

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    #########################################
    # BASE QUERYSETS (OPTIMIZED)
    #########################################

    bookings = Booking.objects.select_related("farmhouse")

    paid_bookings = bookings.filter(payment_status="paid")
    pending_bookings = bookings.filter(payment_status="pending")

    #########################################
    # PLATFORM METRICS
    #########################################

    gross_sales = paid_bookings.aggregate(
        total=Sum("total_amount")
    )["total"] or 0


    commission_expr = ExpressionWrapper(
        F("total_amount") *
        F("farmhouse__commission_percentage") / 100,
        output_field=DecimalField(max_digits=12, decimal_places=2)
    )

    net_revenue = paid_bookings.annotate(
        commission=commission_expr
    ).aggregate(
        total=Sum("commission")
    )["total"] or 0


    overall_pending = pending_bookings.aggregate(
        total=Sum("total_amount")
    )["total"] or 0


    #########################################
    # FARMHOUSE FILTER
    #########################################

    farmhouse_id = request.GET.get("farmhouse")
    farmhouses = Farmhouse.objects.all()

    selected_farmhouse = None

    if farmhouse_id:
        bookings = bookings.filter(farmhouse_id=farmhouse_id)
        paid_bookings = paid_bookings.filter(farmhouse_id=farmhouse_id)
        pending_bookings = pending_bookings.filter(farmhouse_id=farmhouse_id)

        selected_farmhouse = Farmhouse.objects.filter(
            id=farmhouse_id
        ).first()


    #########################################
    # FARMHOUSE METRICS
    #########################################

    fh_total = bookings.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    fh_paid = paid_bookings.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    fh_pending = pending_bookings.aggregate(
        total=Sum("total_amount")
    )["total"] or 0


    fh_today = paid_bookings.filter(
        created_at__date=today
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    fh_week = paid_bookings.filter(
        created_at__date__gte=week_ago
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    fh_month = paid_bookings.filter(
        created_at__date__gte=month_ago
    ).aggregate(total=Sum("total_amount"))["total"] or 0


    booking_count = bookings.count()


    #########################################
    # RECENT BOOKINGS
    #########################################

    recent_bookings = bookings.order_by("-created_at")[:5]


    #########################################
    # ⭐⭐⭐ GRAPH SECTION ⭐⭐⭐
    #########################################

    # Monthly Revenue
    monthly_data = (
        paid_bookings
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )

    months = [m["month"].strftime("%b") for m in monthly_data]
    revenues = [float(m["total"]) for m in monthly_data]


    # Booking Status
    booking_status = (
        bookings
        .values("status")
        .annotate(count=Count("id"))
    )

    booking_status_labels = [b["status"].title() for b in booking_status]
    booking_status_counts = [b["count"] for b in booking_status]


    # Top Farmhouses
    farmhouse_data = (
        paid_bookings
        .values("farmhouse__title")
        .annotate(total=Sum("total_amount"))
        .order_by("-total")[:5]
    )

    fh_names = [f["farmhouse__title"] for f in farmhouse_data]
    fh_totals = [float(f["total"]) for f in farmhouse_data]


    #########################################
    # CONTEXT
    #########################################

    context = {

        "farmhouses": farmhouses,
        "selected_farmhouse": selected_farmhouse,

        # MONEY
        "gross_sales": gross_sales,
        "net_revenue": net_revenue,
        "overall_pending": overall_pending,

        # FARMHOUSE
        "fh_total": fh_total,
        "fh_paid": fh_paid,
        "fh_pending": fh_pending,
        "fh_today": fh_today,
        "fh_week": fh_week,
        "fh_month": fh_month,
        "booking_count": booking_count,
        "recent_bookings": recent_bookings,

        # GRAPHS
        "months": json.dumps(months),
        "revenues": json.dumps(revenues),

        "booking_status_labels": json.dumps(booking_status_labels),
        "booking_status_counts": json.dumps(booking_status_counts),

        "fh_names": json.dumps(fh_names),
        "fh_totals": json.dumps(fh_totals),
    }

    return render(request, "superadmin/dashboard.html", context)


# @superadmin_required
# def all_farmhouses(request):
#     farmhouses = Farmhouse.objects.select_related("user", "location")

#     return render(
#         request,
#         "superadmin/farmhouses.html",
#         {"farmhouses": farmhouses}
#     )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from farmhouse.models import Farmhouse, FarmhousePricing
from superadmin_dashboard.forms import FarmhouseForm, FarmhousePricingForm,FarmhouseImageForm


# def superadmin_required(user):
#     return user.is_superuser


# ===============================
# LIST
# ===============================
# @superadmin_required
# # @user_passes_test(superadmin_required)
# def farmhouse_list(request):
#         # ✅ permission check
#     if not is_farmhouse_staff(request.user) and not request.user.is_superuser:
#         return HttpResponseForbidden("Not allowed")

#     farmhouses = Farmhouse.objects.all()
#     return render(
#         request,
#         "superadmin/farmhouses.html",
#         {"farmhouses": farmhouses}
#     )


from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render


@superadmin_required
def farmhouse_list(request):

    if not is_farmhouse_staff(request.user) and not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    query = request.GET.get("q", "").strip()

    farmhouses = Farmhouse.objects.select_related("user").all()

    if query:
        farmhouses = farmhouses.filter(
            Q(title__icontains=query) |
            Q(user__email__icontains=query)
        )

    # context = {
    #     "farmhouses": farmhouses,
    #     "query": query
    # }

    # return render(request, "superadmin/farmhouses.html", context)
    # 🔹 PAGINATION
    paginator = Paginator(farmhouses, 10)  # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "farmhouses": page_obj,
        "page_obj": page_obj,
        "query": query
    }

    return render(request, "superadmin/farmhouses.html", context)
# ===============================
# ADD
# ===============================

@superadmin_required
def farmhouse_add(request):

    if request.method == "POST":
        form = FarmhouseForm(request.POST)
        pricing_form = FarmhousePricingForm(request.POST)

        if form.is_valid() and pricing_form.is_valid():

            farmhouse = form.save()

            pricing = pricing_form.save(commit=False)
            pricing.farmhouse = farmhouse
            pricing.save()

            images = request.FILES.getlist("gallery_images")
            for i, img in enumerate(images):
                FarmhouseImage.objects.create(
                    farmhouse=farmhouse,
                    image=img,
                    is_primary=(i == 0)
                )

            return redirect("superadmin-farmhouses")

    else:
        form = FarmhouseForm()
        pricing_form = FarmhousePricingForm()

    return render(request, "superadmin/farmhouse_add.html", {
        "form": form,
        "pricing_form": pricing_form
    })
    

@superadmin_required
# @user_passes_test(superadmin_required)
def farmhouse_edit(request, id):

    farmhouse = get_object_or_404(Farmhouse, id=id)
    pricing, _ = FarmhousePricing.objects.get_or_create(farmhouse=farmhouse)

    if request.method == "POST":
        form = FarmhouseForm(request.POST, instance=farmhouse)
        pricing_form = FarmhousePricingForm(request.POST, instance=pricing)

        if form.is_valid() and pricing_form.is_valid():
            form.save()
            pricing_form.save()

            # ✅ ADD NEW IMAGES
            images = request.FILES.getlist("gallery_images")
            for img in images:
                FarmhouseImage.objects.create(
                    farmhouse=farmhouse,
                    image=img
                )

            return redirect("superadmin-farmhouses")

    else:
        form = FarmhouseForm(instance=farmhouse)
        pricing_form = FarmhousePricingForm(instance=pricing)

    return render(request, "superadmin/farmhouse_add.html", {
        "form": form,
        "pricing_form": pricing_form,
        "farmhouse": farmhouse
    })
from booking.models import Invoice
@superadmin_required
def admin_view_invoice(request, booking_id):

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

# ===============================
# DELETE
# ===============================
@superadmin_required
# @user_passes_test(superadmin_required)
def farmhouse_delete(request, id):
    farmhouse = get_object_or_404(Farmhouse, id=id)
    farmhouse.delete()
    return redirect("superadmin-farmhouses")
# ===========================================================






from django.shortcuts import render, redirect, get_object_or_404
from farmhouse.models import Banner, Location, Amenity
from .forms import BannerForm, LocationForm, AmenityForm

# ================= BANNERS =================

# def banner_list(request):
#     banners = Banner.objects.all()
#     return render(request, "superadmin/banners/banner_list.html", {"banners": banners})
@superadmin_required
def banner_list(request):
    items = Banner.objects.all()

    return render(request, "superadmin/banners/banner_list.html", {
        "items": items,
        "title": "Banners",
        "add_url": "banner_add",   # ✅ URL name
    })

@superadmin_required
def banner_create(request):
    form = BannerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("banner-list")
    return render(request, "superadmin/banners/banner_form.html", {"form": form})

@superadmin_required
def banner_update(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    form = BannerForm(request.POST or None, request.FILES or None, instance=banner)
    if form.is_valid():
        form.save()
        return redirect("banner-list")
    return render(request, "superadmin/banners/banner_form.html", {"form": form})

@superadmin_required
def banner_delete(request, pk):
    banner = get_object_or_404(Banner, pk=pk)

    if request.method == "POST":
        banner.delete()
        return redirect("banner-list")


# def banner_delete(request, pk):
#     banner = get_object_or_404(Banner, pk=pk)
#     if request.method == "POST":
#         banner.delete()
#         return redirect("banner-list")
#     return render(request, "superadmin/banners/banner_delete.html", {"obj": banner})


# ================= LOCATIONS =================

# def location_list(request):
#     locations = Location.objects.all()
#     return render(request, "superadmin/locations/locations_list.html", {"locations": locations})
@superadmin_required
def location_list(request):
    # items = Location.objects.all()
    # return render(request, "superadmin/locations/location_list.html", {
    #     "items": items,
    #     "title": "Locations",
    #     "add_url": "location-add",
    # })
    locations = Location.objects.all().order_by("name")

    paginator = Paginator(locations, 10)   # 10 locations per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "superadmin/locations/location_list.html", {
        "items": page_obj,
        "page_obj": page_obj,
        "title": "Locations",
        "add_url": "location-add",
    })
    
    
@superadmin_required
def location_create(request):
    form = LocationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("location-list")
    return render(request, "superadmin/locations/location_form.html", {"form": form})

@superadmin_required
def location_update(request, pk):
    obj = get_object_or_404(Location, pk=pk)
    form = LocationForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("location-list")
    return render(request, "superadmin/locations/location_form.html", {"form": form})

@superadmin_required
def location_delete(request, pk):
    obj = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("location-list")
    # return render(request, "superadmin/locations/location_delete.html", {"obj": obj})


# ================= AMENITIES =================

# def amenity_list(request):
#     amenities = Amenity.objects.all()
#     return render(request, "superadmin/amenities/amenities_list.html", {"amenities": amenities})

@superadmin_required
def amenity_list(request):
    amenities = Amenity.objects.all().order_by("name")

    paginator = Paginator(amenities, 10)  # 10 items per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "superadmin/amenities/amenities_list.html", {
        "items": page_obj,
        "page_obj": page_obj,
        "title": "Amenities",
        "add_url": "amenity-add",
    })
    # items = Amenity.objects.all()
    # return render(request, "superadmin/amenities/amenities_list.html", {
    #     "items": items,
    #     "title": "Amenities",
    #     "add_url": "amenity-add",
    # })

@superadmin_required
def amenity_create(request):
    form = AmenityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("amenity-list")
    return render(request, "superadmin/amenities/amenities_form.html", {"form": form})

@superadmin_required
def amenity_update(request, pk):
    obj = get_object_or_404(Amenity, pk=pk)
    form = AmenityForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("amenity-list")
    return render(request, "superadmin/amenities/amenities_form.html", {"form": form})

@superadmin_required
def amenity_delete(request, pk):
    obj = get_object_or_404(Amenity, pk=pk)

    if request.method == "POST":
        obj.delete()

    return redirect("amenity-list")



@superadmin_required
def category_list(request):
    categories = BlogCategory.objects.all()
    return render(request, "superadmin/blog/category_list.html", {
        "categories": categories
    })


@superadmin_required
def category_add(request):
    if request.method == "POST":
        BlogCategory.objects.create(
            name=request.POST.get("name"),
            is_active=True if request.POST.get("is_active") else False
        )
        messages.success(request, "Category added successfully")
        return redirect("category_list")

    return render(request, "superadmin/blog/category_form.html")


@superadmin_required
def category_edit(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)

    if request.method == "POST":
        category.name = request.POST.get("name")
        category.is_active = True if request.POST.get("is_active") else False
        category.save()

        messages.success(request, "Category updated")
        return redirect("category_list")

    return render(request, "superadmin/blog/category_form.html", {
        "category": category
    })


@superadmin_required
def category_delete(request, pk):
    BlogCategory.objects.filter(pk=pk).delete()
    messages.success(request, "Category deleted")
    return redirect("category_list")


# ===============================
# TAG CRUD
# ===============================

@superadmin_required
def tag_list(request):
    tags = BlogTag.objects.all()
    return render(request, "superadmin/blog/tag_list.html", {"tags": tags})


@superadmin_required
def tag_add(request):
    if request.method == "POST":
        BlogTag.objects.create(
            name=request.POST.get("name")
        )
        messages.success(request, "Tag added")
        return redirect("tag_list")

    return render(request, "superadmin/blog/tag_form.html")


@superadmin_required
def tag_edit(request, pk):
    tag = get_object_or_404(BlogTag, pk=pk)

    if request.method == "POST":
        tag.name = request.POST.get("name")
        tag.save()
        messages.success(request, "Tag updated")
        return redirect("tag_list")

    return render(request, "superadmin/blog/tag_form.html", {"tag": tag})


@superadmin_required
def tag_delete(request, pk):
    BlogTag.objects.filter(pk=pk).delete()
    messages.success(request, "Tag deleted")
    return redirect("tag_list")


# ===============================
# BLOG CRUD
# ===============================

@superadmin_required
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, "superadmin/blog/blog_list.html", {
        "blogs": blogs
    })


# @login_required
# @user_passes_test(superadmin_required)
# def blog_add(request):
#     categories = BlogCategory.objects.filter(is_active=True)
#     tags = BlogTag.objects.all()

#     if request.method == "POST":
#         blog = Blog.objects.create(
#             title=request.POST.get("title"),
#             category_id=request.POST.get("category"),
#             short_description=request.POST.get("short_description"),
#             content=request.POST.get("content"),
#             read_time=request.POST.get("read_time"),
#             is_published=True if request.POST.get("is_published") else False,
#         )

#         if request.FILES.get("image"):
#             blog.image = request.FILES.get("image")
#             blog.save()

#         tag_ids = request.POST.getlist("tags")
#         blog.tags.set(tag_ids)

#         messages.success(request, "Blog created successfully")
#         return redirect("blog_list")

#     return render(request, "superadmin/blog/blog_form.html", {
#         "categories": categories,
#         "tags": tags
#     })


# @login_required
# @user_passes_test(superadmin_required)
# def blog_edit(request, pk):
#     blog = get_object_or_404(Blog, pk=pk)
#     categories = BlogCategory.objects.filter(is_active=True)
#     tags = BlogTag.objects.all()

#     if request.method == "POST":
#         blog.title = request.POST.get("title")
#         blog.category_id = request.POST.get("category")
#         blog.short_description = request.POST.get("short_description")
#         blog.content = request.POST.get("content")
#         blog.read_time = request.POST.get("read_time")
#         blog.is_published = True if request.POST.get("is_published") else False

#         if request.FILES.get("image"):
#             blog.image = request.FILES.get("image")

#         blog.save()
#         blog.tags.set(request.POST.getlist("tags"))

#         messages.success(request, "Blog updated successfully")
#         return redirect("blog_list")

#     return render(request, "superadmin/blog/blog_form.html", {
#         "blog": blog,
#         "categories": categories,
#         "tags": tags
#     })
@superadmin_required
def blog_add(request):

    categories = BlogCategory.objects.filter(is_active=True)
    tags = BlogTag.objects.all()

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Blog created successfully")
            return redirect("blog_list")
    else:
        form = BlogForm()

    return render(request, "superadmin/blog/blog_form.html", {
        "form": form,
        "categories": categories,
        "tags": tags
    })
@superadmin_required
def blog_edit(request, pk):

    blog = get_object_or_404(Blog, pk=pk)
    categories = BlogCategory.objects.filter(is_active=True)
    tags = BlogTag.objects.all()

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully")
            return redirect("blog_list")
    else:
        form = BlogForm(instance=blog)

    return render(request, "superadmin/blog/blog_form.html", {
        "form": form,
        "categories": categories,
        "tags": tags
    })



@superadmin_required
def blog_delete(request, pk):
    Blog.objects.filter(pk=pk).delete()
    messages.success(request, "Blog deleted")
    return redirect("blog_list")


# ===============================
# COMMENTS MODERATION
# ===============================

@superadmin_required
def comment_list(request):
    comments = BlogComment.objects.select_related("blog").order_by("-created_at")
    return render(request, "superadmin/blog/comment_list.html", {
        "comments": comments
    })


@superadmin_required
def comment_toggle(request, pk):
    comment = get_object_or_404(BlogComment, pk=pk)
    comment.is_active = not comment.is_active
    comment.save()
    return redirect("comment_list")


# cms views

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from cms.models import *
from superadmin_dashboard.forms import *


def paginate(request, queryset):
    paginator = Paginator(queryset, 10)
    page = request.GET.get("page")
    return paginator.get_page(page)


# ================= CHOOSE SERVICES =================
@superadmin_required
def choose_services_list(request):
    services = paginate(request, Choos_Services.objects.all())
    return render(request, "superadmin/cms/choose_services_list.html", {"services": services})

@superadmin_required
def choose_services_add(request):
    form = ChooseServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Service added successfully")
        return redirect("choose_services_list")
    return render(request, "superadmin/cms/choose_services_form.html", {"form": form})

@superadmin_required
def choose_services_edit(request, id):
    obj = get_object_or_404(Choos_Services, id=id)
    form = ChooseServiceForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Service updated successfully")
        return redirect("choose_services_list")
    return render(request, "superadmin/cms/choose_services_form.html", {"form": form})

@superadmin_required
def choose_services_delete(request, id):
    get_object_or_404(Choos_Services, id=id).delete()
    messages.success(request, "Deleted successfully")
    return redirect("choose_services_list")


# ================= FACILITIES =====================================
@superadmin_required
def facilities_list(request):
    facilities = paginate(request, Facilities.objects.all())
    return render(request, "superadmin/cms/facility_list.html", {"facilities": facilities})

@superadmin_required
def facilities_add(request):
    form = FacilityForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Facility added")
        return redirect("facilities_list")
    return render(request, "superadmin/cms/facility_form.html", {"form": form})

@superadmin_required
def facilities_edit(request, id):
    obj = get_object_or_404(Facilities, id=id)
    form = FacilityForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Facility updated")
        return redirect("facilities_list")
    return render(request, "superadmin/cms/facility_form.html", {"form": form})

@superadmin_required
def facilities_delete(request, id):
    get_object_or_404(Facilities, id=id).delete()
    messages.success(request, "Deleted successfully")
    return redirect("facilities_list")


# ================= OUR FACILITY =================
@superadmin_required
def our_facility_list(request):
    items = paginate(request, OurFacility.objects.all())
    return render(request, "superadmin/cms/our_facility_list.html", {"items": items})

@superadmin_required
def our_facility_add(request):
    form = OurFacilityForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Facility added")
        return redirect("our_facility_list")
    return render(request, "superadmin/cms/our_facility_form.html", {"form": form})

@superadmin_required
def our_facility_edit(request, id):
    obj = get_object_or_404(OurFacility, id=id)
    form = OurFacilityForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated successfully")
        return redirect("our_facility_list")
    return render(request, "superadmin/cms/our_facility_form.html", {"form": form})

@superadmin_required
def our_facility_delete(request, id):
    get_object_or_404(OurFacility, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("our_facility_list")


# ================= WHO WE ARE =================
@superadmin_required
def who_we_are_list(request):
    items = paginate(request, WhoWeAre.objects.all())
    return render(request, "superadmin/cms/who_we_are_list.html", {"items": items})

@superadmin_required
def who_we_are_add(request):
    form = WhoWeAreForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Added")
        return redirect("who_we_are_list")
    return render(request, "superadmin/cms/who_we_are_form.html", {"form": form})

@superadmin_required
def who_we_are_edit(request, id):
    obj = get_object_or_404(WhoWeAre, id=id)
    form = WhoWeAreForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect("who_we_are_list")
    return render(request, "superadmin/cms/who_we_are_form.html", {"form": form})

@superadmin_required
def who_we_are_delete(request, id):
    get_object_or_404(WhoWeAre, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("who_we_are_list")


# ================= ABOUT SECTION =================
@superadmin_required
def about_section_list(request):
    items = paginate(request, AboutSection.objects.all())
    return render(request, "superadmin/cms/about_section_list.html", {"items": items})

@superadmin_required
def about_section_add(request):
    form = AboutSectionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Saved")
        return redirect("about_section_list")
    return render(request, "superadmin/cms/about_section_form.html", {"form": form})

@superadmin_required
def about_section_edit(request, id):
    obj = get_object_or_404(AboutSection, id=id)
    form = AboutSectionForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect("about_section_list")
    return render(request, "superadmin/cms/about_section_form.html", {"form": form})

@superadmin_required
def about_section_delete(request, id):
    get_object_or_404(AboutSection, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("about_section_list")


# ================= ABOUT FEATURE =================
@superadmin_required
def about_feature_list(request):
    items = paginate(request, AboutFeature.objects.all())
    return render(request, "superadmin/cms/about_feature_list.html", {"items": items})

@superadmin_required
def about_feature_add(request):
    form = AboutFeatureForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Added")
        return redirect("about_feature_list")
    return render(request, "superadmin/cms/about_feature_form.html", {"form": form})

@superadmin_required
def about_feature_edit(request, id):
    obj = get_object_or_404(AboutFeature, id=id)
    form = AboutFeatureForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect("about_feature_list")
    return render(request, "superadmin/cms/about_feature_form.html", {"form": form})

@superadmin_required
def about_feature_delete(request, id):
    get_object_or_404(AboutFeature, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("about_feature_list")


# ================= ABOUT WHO WE ARE =================
@superadmin_required
def about_who_we_are_list(request):
    items = paginate(request, AboutWhoWeAre.objects.all())
    return render(request, "superadmin/cms/about_who_we_are_list.html", {"items": items})

@superadmin_required
def about_who_we_are_add(request):
    form = AboutWhoWeAreForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Saved")
        return redirect("about_who_we_are_list")
    return render(request, "superadmin/cms/about_who_we_are_form.html", {"form": form})

@superadmin_required
def about_who_we_are_edit(request, id):
    obj = get_object_or_404(AboutWhoWeAre, id=id)
    form = AboutWhoWeAreForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect("about_who_we_are_list")
    return render(request, "superadmin/cms/about_who_we_are_form.html", {"form": form})

@superadmin_required
def about_who_we_are_delete(request, id):
    get_object_or_404(AboutWhoWeAre, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("about_who_we_are_list")

# coupon

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from coupon.models import Coupon, CouponUsage
from .forms import CouponForm



# ================= COUPON =================
@superadmin_required
def coupon_list(request):
    coupons = paginate(request, Coupon.objects.all())
    return render(request, "superadmin/coupons/coupon_list.html", {
        "coupons": coupons
    })

@superadmin_required
def coupon_add(request):
    form = CouponForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Coupon created successfully")
        return redirect("coupon_list")
    return render(request, "superadmin/coupons/coupon_form.html", {
        "form": form,
        "title": "Add Coupon"
    })

@superadmin_required
def coupon_edit(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    form = CouponForm(request.POST or None, instance=coupon)
    if form.is_valid():
        form.save()
        messages.success(request, "Coupon updated successfully")
        return redirect("coupon_list")
    return render(request, "superadmin/coupons/coupon_form.html", {
        "form": form,
        "title": "Edit Coupon"
    })

@superadmin_required
def coupon_delete(request, id):
    get_object_or_404(Coupon, id=id).delete()
    messages.success(request, "Coupon deleted")
    return redirect("coupon_list")


# ================= COUPON USAGE =================
@superadmin_required
def coupon_usage_list(request):
    usages = paginate(request, CouponUsage.objects.select_related("coupon", "user"))
    return render(request, "superadmin/coupons/coupon_usage_list.html", {
        "usages": usages
    })


# =============================
from django.http import HttpResponseForbidden

def is_farmhouse_staff(user):
    """
    Farmhouse staff = staff + farmhouse_user true
    """
    return (
        user.is_authenticated and
        user.is_staff and
        user.farmhouse_user
    )


@superadmin_required
def admin_user_list(request):
    users = User.objects.all().order_by("-id")

    return render(request, "superadmin/user/user_list.html", {
        "users": users
    })


@superadmin_required
def admin_user_add(request):
    form = AdminUserForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("admin_user_list")

    return render(request, "superadmin/user/user_form.html", {
        "form": form,
        "title": "Add User"
    })
from django.contrib.auth import update_session_auth_hash


@superadmin_required
def admin_user_edit(request, id):
    user = get_object_or_404(User, id=id)
    form = AdminUserForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect("admin_user_list")

    return render(request, "superadmin/user/user_form.html", {
        "form": form,
        "title": "Edit User"
    })

@superadmin_required
def admin_user_delete(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect("admin_user_list")


# ==============
from contact.models import ContactInfo, ContactMessage
from superadmin_dashboard.forms import ContactInfoForm

@superadmin_required
def contact_info_list(request):
    items = ContactInfo.objects.all().order_by("-id")
    paginator = Paginator(items, 10)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "superadmin/contact/info_list.html", {
        "items": page
    })

@superadmin_required
def contact_info_add(request):
    form = ContactInfoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("contact_info_list")

    return render(request, "superadmin/contact/info_form.html", {
        "form": form,
        "title": "Add Contact Info"
    })


@superadmin_required
def contact_info_edit(request, id):
    obj = get_object_or_404(ContactInfo, id=id)
    form = ContactInfoForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect("contact_info_list")

    return render(request, "superadmin/contact/info_form.html", {
        "form": form,
        "title": "Edit Contact Info"
    })


@superadmin_required
def contact_info_delete(request, id):
    obj = get_object_or_404(ContactInfo, id=id)
    obj.delete()
    return redirect("contact_info_list")







@superadmin_required
def contact_message_list(request):
    messages = ContactMessage.objects.all().order_by("-created_at")
    paginator = Paginator(messages, 10)
    page = paginator.get_page(request.GET.get("page"))

    return render(request, "superadmin/contact/message_list.html", {
        "messages": page
    })


@superadmin_required
def contact_message_delete(request, id):
    msg = get_object_or_404(ContactMessage, id=id)
    msg.delete()
    return redirect("contact_message_list")



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator

from booking.models import Booking
from superadmin_dashboard.forms import AdminBookingForm
from booking.models import Booking
from farmhouse.models import Farmhouse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q


@superadmin_required
def admin_booking_list(request):

    bookings = Booking.objects.select_related(
        "farmhouse",
        "user"
    ).order_by("-created_at")

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
    # FARMHOUSE FILTER ⭐⭐⭐
    ###################################

    farmhouse_id = request.GET.get("farmhouse")

    if farmhouse_id:
        bookings = bookings.filter(farmhouse_id=farmhouse_id)

    ###################################
    # PAGINATION ⭐⭐⭐
    ###################################

    paginator = Paginator(bookings, 10)
    page = request.GET.get("page")
    bookings = paginator.get_page(page)

    ###################################
    # SEND FARMHOUSES TO TEMPLATE
    ###################################

    farmhouses = Farmhouse.objects.all()

    return render(
        request,
        "superadmin/booking/list.html",
        {
            "bookings": bookings,
            "farmhouses": farmhouses,
        }
    )


from django.http import JsonResponse
from decimal import Decimal
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
import json


@superadmin_required
@require_POST
def admin_calculate_booking_price(request):
    data = json.loads(request.body)
    farmhouse_id = data.get("farmhouse")
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    extra_guest_count = int(data.get("extra_guest_count", 0))
    coupon_id = data.get("coupon")

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

    discount = Decimal("0.00")

    if coupon_id:

        coupon = Coupon.objects.filter(
            id=coupon_id,
            is_active=True
        ).first()

        if coupon and subtotal >= coupon.min_booking_amount:
            discount = coupon.calculate_discount(subtotal)

    total = subtotal - discount

    return JsonResponse({
        "subtotal": float(subtotal),
        "discount": float(discount),
        "total": float(total)
    })

from decimal import Decimal
from datetime import datetime, timedelta
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q

@superadmin_required
def admin_booking_create(request):

    if request.method == "POST":

        form = AdminBookingForm(request.POST)

        if form.is_valid():

            ########################################
            # DO NOT SAVE YET
            ########################################
            booking = form.save(commit=False)

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
            discount = Decimal("0.00")

            if booking.coupon_applied:
                coupon = booking.coupon_applied

                if coupon.is_active and subtotal >= coupon.min_booking_amount:
                    discount = coupon.calculate_discount(subtotal)

            ########################################
            # FINAL AMOUNTS
            ########################################
            booking.sub_total = subtotal
            booking.disc_price = discount
            booking.tax_price = Decimal("0.00")   # add GST if needed
            booking.total_amount = subtotal - discount
            booking.remaining_amount = booking.total_amount

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
        form = AdminBookingForm()

    return render(
        request,
        "superadmin/booking/form.html",
        {"form": form}
    )

    
    
    

# @staff_member_required
# def admin_booking_detail(request, pk):

#     booking = get_object_or_404(
#         Booking.objects.select_related(
#             "farmhouse",
#             "user"
#         ),
#         pk=pk
#     )

#     return render(
#         request,
#         "superadmin/booking/detail.html",
#         {"booking": booking}
#     )
from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction


# @staff_member_required
# def admin_booking_detail(request, pk):

#     booking = get_object_or_404(
#         Booking.objects.select_related(
#             "farmhouse",
#             "user"
#         ),
#         pk=pk
#     )

#     ###################################
#     # QUICK STATUS UPDATE
#     ###################################

#     if request.method == "POST":

#         new_status = request.POST.get("status")

#         if new_status and new_status != booking.status:

#             booking.status = new_status
#             booking.save()

#             transaction.on_commit(
#                 lambda: booking.send_booking_email(
#                     booking.status,
#                     request
#                 )
#             )

#             messages.success(
#                 request,
#                 "Booking status updated successfully ✅"
#             )

#             return redirect(
#                 "admin-booking-detail",
#                 pk=booking.pk
#             )

#     return render(
#         request,
#         "superadmin/booking/detail.html",
#         {"booking": booking}
#     )
from decimal import Decimal

@superadmin_required
def admin_booking_detail(request, pk):

    booking = get_object_or_404(
        Booking.objects.select_related(
            "farmhouse",
            "user"
        ),
        pk=pk
    )

    ###################################
    # STATUS + PAYMENT UPDATE
    ###################################

    if request.method == "POST":

        new_status = request.POST.get("status")
        new_payment_status = request.POST.get("payment_status")

        status_changed = False

        # BOOKING STATUS
        if new_status and new_status != booking.status:
            booking.status = new_status
            status_changed = True

        # PAYMENT STATUS
        if new_payment_status and new_payment_status != booking.payment_status:

            booking.payment_status = new_payment_status

            ###################################
            # AUTO CALCULATE REMAINING 🔥
            ###################################

            if new_payment_status == "paid":
                booking.remaining_amount = 0

            elif new_payment_status == "partial":
                paid_amount = booking.total_amount * Decimal("0.30")
                booking.remaining_amount = booking.total_amount - paid_amount

            else:
                booking.remaining_amount = booking.total_amount

        booking.save()

        ###################################
        # SEND EMAIL ONLY IF STATUS CHANGED
        ###################################

        if status_changed:
            transaction.on_commit(
                lambda: booking.send_booking_email(
                    booking.status,
                    request
                )
            )

        messages.success(
            request,
            "Booking updated successfully ✅"
        )

        return redirect(
            "admin-booking-detail",
            pk=booking.pk
        )

    return render(
        request,
        "superadmin/booking/detail.html",
        {"booking": booking}
    )


@superadmin_required
def admin_booking_update(request, pk):

    booking = get_object_or_404(Booking, pk=pk)

    old_status = booking.status

    if request.method == "POST":

        form = AdminBookingForm(
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
        form = AdminBookingForm(instance=booking)

    return render(
        request,
        "superadmin/booking/form.html",
        {"form": form}
    )


@superadmin_required
def admin_booking_cancel(request, pk):

    booking = get_object_or_404(Booking, pk=pk)

    try:
        booking.cancel_booking(user=request.user)

        messages.success(
            request,
            "Booking cancelled successfully!"
        )

    except Exception as e:

        messages.error(request, str(e))

    return redirect("admin-bookings")









# 

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from booking.models import BlockedDate
from django.shortcuts import redirect
from django.contrib import messages
from superadmin_dashboard.forms import BlockedDateForm

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import BlockedDateForm
from django.contrib.admin.views.decorators import staff_member_required

import json
from booking.models import BlockedDate, Booking
from datetime import timedelta

import json
from datetime import timedelta
from django.http import JsonResponse



@superadmin_required
def blocked_dates_list(request):

    blocked = BlockedDate.objects.select_related(
        "farmhouse"
    ).order_by("-created_at")

    return render(
        request,
        "superadmin/blocked/list.html",
        {"blocked": blocked}
    )



# @superadmin_required
# def blocked_dates_create(request):

#     ###################################
#     # AJAX CALL (farmhouse selected)
#     ###################################
#     if request.GET.get("farmhouse"):

#         farmhouse_id = request.GET.get("farmhouse")

#         blocked_ranges = []

#         # ADMIN BLOCKS
#         blocks = BlockedDate.objects.filter(
#             farmhouse_id=farmhouse_id
#         )

#         for b in blocks:
#             blocked_ranges.append({
#                 "from": b.start_date.strftime("%Y-%m-%d"),
#                 "to": (b.end_date - timedelta(days=1)).strftime("%Y-%m-%d")
#             })

#         # BOOKINGS
#         bookings = Booking.objects.filter(
#             farmhouse_id=farmhouse_id,
#             status__in=["pending","confirmed"]
#         )

#         for booking in bookings:
#             blocked_ranges.append({
#                 "from": booking.check_in.strftime("%Y-%m-%d"),
#                 "to": (booking.check_out - timedelta(days=1)).strftime("%Y-%m-%d")
#             })

#         return JsonResponse(blocked_ranges, safe=False)

#     ###################################
#     # NORMAL FORM
#     ###################################

#     if request.method == "POST":

#         form = BlockedDateForm(request.POST)

#         if form.is_valid():
#             form.save()

#             messages.success(
#                 request,
#                 "Dates blocked successfully!"
#             )

#             return redirect("blocked-dates")

#     else:
#         form = BlockedDateForm()

#     return render(
#         request,
#         "superadmin/blocked/form.html",
#         {"form": form}
#     )




from datetime import timedelta
from django.http import JsonResponse
from datetime import timedelta
from django.http import JsonResponse
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import BlockedDateForm
from booking.models import BlockedDate, Booking
from farmhouse.models import FarmhouseFacilities


from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from .models import BlockedDate, Booking
# from .forms import BlockedDateForm


###############################################
# CREATE
###############################################
@superadmin_required
def blocked_dates_create(request):

    # AJAX
    if request.GET.get("farmhouse"):
        farmhouse_id = request.GET.get("farmhouse")
        blocked_ranges = []

        # ADMIN BLOCKS (exclusive end)
        blocks = BlockedDate.objects.filter(farmhouse_id=farmhouse_id)
        for b in blocks:
            blocked_ranges.append({
                "from": b.start_date.strftime("%Y-%m-%d"),
                "to": b.end_date.strftime("%Y-%m-%d")
            })

        # BOOKINGS (exclusive end)
        bookings = Booking.objects.filter(
            farmhouse_id=farmhouse_id,
            status__in=["pending", "confirmed"]
        )
        for booking in bookings:
            blocked_ranges.append({
                "from": booking.check_in.strftime("%Y-%m-%d"),
                "to": booking.check_out.strftime("%Y-%m-%d")
            })

        return JsonResponse(blocked_ranges, safe=False)

    # FORM
    if request.method == "POST":
        form = BlockedDateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dates blocked successfully!")
            return redirect("blocked-dates")
    else:
        form = BlockedDateForm()

    return render(request, "superadmin/blocked/form.html", {"form": form})


###############################################
# UPDATE
###############################################
@superadmin_required
def blocked_dates_update(request, pk):

    blocked = get_object_or_404(BlockedDate, pk=pk)

    # AJAX
    if request.GET.get("farmhouse"):
        farmhouse_id = request.GET.get("farmhouse")
        blocked_ranges = []

        blocks = BlockedDate.objects.filter(
            farmhouse_id=farmhouse_id
        ).exclude(pk=blocked.pk)

        for b in blocks:
            blocked_ranges.append({
                "from": b.start_date.strftime("%Y-%m-%d"),
                "to": b.end_date.strftime("%Y-%m-%d")
            })

        bookings = Booking.objects.filter(
            farmhouse_id=farmhouse_id,
            status__in=["pending", "confirmed"]
        )
        for booking in bookings:
            blocked_ranges.append({
                "from": booking.check_in.strftime("%Y-%m-%d"),
                "to": booking.check_out.strftime("%Y-%m-%d")
            })

        return JsonResponse(blocked_ranges, safe=False)

    # FORM UPDATE
    if request.method == "POST":
        form = BlockedDateForm(request.POST, instance=blocked)
        if form.is_valid():
            form.save()
            messages.success(request, "Blocked dates updated!")
            return redirect("blocked-dates")
    else:
        form = BlockedDateForm(instance=blocked)

    return render(request, "superadmin/blocked/form.html", {"form": form})

# @superadmin_required
# def blocked_dates_update(request, pk):

#     blocked = get_object_or_404(
#         BlockedDate,
#         pk=pk
#     )

#     ###################################
#     # ✅ AJAX FOR CALENDAR
#     ###################################
#     if request.GET.get("farmhouse"):

#         farmhouse_id = request.GET.get("farmhouse")

#         blocked_ranges = []

#         ###################################
#         # BLOCKED DATES
#         ###################################

#         blocks = BlockedDate.objects.filter(
#             farmhouse_id=farmhouse_id
#         ).exclude(id=blocked.id)   # ⭐ VERY IMPORTANT

#         for b in blocks:
#             blocked_ranges.append({
#                 "from": b.start_date.strftime("%Y-%m-%d"),
#                 # "to": (b.end_date - timedelta(days=1)).strftime("%Y-%m-%d")
#                 "to": b.end_date.strftime("%Y-%m-%d") 

#             })

#         ###################################
#         # BOOKINGS
#         ###################################
#         bookings = Booking.objects.filter(
#             farmhouse_id=farmhouse_id,
#             status__in=["pending","confirmed"]
#         )

#         for booking in bookings:
#             blocked_ranges.append({
#                 "from": booking.check_in.strftime("%Y-%m-%d"),
#                 "to": (booking.check_out - timedelta(days=1)).strftime("%Y-%m-%d")
#             })

#         return JsonResponse(blocked_ranges, safe=False)

#     ###################################
#     # NORMAL UPDATE
#     ###################################

#     if request.method == "POST":

#         form = BlockedDateForm(
#             request.POST,
#             instance=blocked
#         )

#         if form.is_valid():
#             form.save()

#             messages.success(
#                 request,
#                 "Blocked dates updated!"
#             )

#             return redirect("blocked-dates")

#     else:
#         form = BlockedDateForm(instance=blocked)

#     return render(
#         request,
#         "superadmin/blocked/form.html",
#         {"form": form}
#     )



@superadmin_required
def blocked_dates_delete(request, pk):

    blocked = get_object_or_404(
        BlockedDate,
        pk=pk
    )

    blocked.delete()

    messages.success(
        request,
        "Blocked dates removed!"
    )

    return redirect("blocked-dates")


# ======================


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from booking.models import FarmhousePaymentPolicy
from superadmin_dashboard.forms import FarmhousePaymentPolicyForm


def payment_policy_create(request):
    if request.method == "POST":
        form = FarmhousePaymentPolicyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment Policy Created Successfully")
            return redirect("payment_policy_list")
    else:
        form = FarmhousePaymentPolicyForm()

    return render(request, "superadmin/payment_policy/form.html", {
        "form": form
    })


def payment_policy_list(request):
    policies = FarmhousePaymentPolicy.objects.select_related("farmhouse")

    return render(request, "superadmin/payment_policy/list.html", {
        "policies": policies
    })
    
def payment_policy_update(request, pk):
    policy = get_object_or_404(FarmhousePaymentPolicy, pk=pk)

    if request.method == "POST":
        form = FarmhousePaymentPolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment Policy Updated Successfully")
            return redirect("payment_policy_list")
    else:
        form = FarmhousePaymentPolicyForm(instance=policy)

    return render(request, "superadmin/payment_policy/form.html", {
        "form": form
    })



@superadmin_required
def payment_policy_delete(request, pk):

    policy = get_object_or_404(
        FarmhousePaymentPolicy,
        pk=pk
    )

    farmhouse_name = policy.farmhouse  # optional (for message)

    policy.delete()

    messages.success(
        request,
        f"Payment policy for '{farmhouse_name}' deleted successfully!"
    )

    return redirect("payment_policy_list")




from django.core.paginator import Paginator
# def facility_list(request):
#     facilities = FarmhouseFacilities.objects.all().order_by("-id")

#     return render(request, "superadmin/facilities/list.html", {
#         "facilities": facilities
#     })




def facility_list(request):
    facility_qs = FarmhouseFacilities.objects.all().order_by("-id")

    paginator = Paginator(facility_qs, 10)  # 🔹 10 per page
    page_number = request.GET.get("page")
    facilities = paginator.get_page(page_number)

    return render(request, "superadmin/facilities/list.html", {
        "facilities": facilities
    })



def facility_create(request):
    form = FacilityForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Facility created successfully ✅")
        return redirect("facility-list")

    return render(request, "superadmin/facilities/form.html", {
        "form": form,
        "title": "Add Facility"
    })


def facility_update(request, pk):
    facility = get_object_or_404(FarmhouseFacilities, pk=pk)

    form = FacilityForm(request.POST or None, instance=facility)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Facility updated successfully ✏️")
        return redirect("facility-list")

    return render(request, "superadmin/facilities/form.html", {
        "form": form,
        "title": "Edit Facility"
    })


def facility_delete(request, pk):
    facility = get_object_or_404(FarmhouseFacilities, pk=pk)

    facility.delete()
    messages.success(request, "Facility deleted successfully 🗑️")

    return redirect("facility-list")



from django.shortcuts import render, redirect, get_object_or_404
from booking.models import CancelReason
from .forms import CancelReasonForm


# LIST
def cancel_reason_list(request):
    reasons = CancelReason.objects.all().order_by("-id")
    return render(request, "superadmin/cancel_reason/list.html", {"reasons": reasons})


# CREATE
def cancel_reason_create(request):
    form = CancelReasonForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("cancel_reason_list")
    return render(request, "superadmin/cancel_reason/form.html", {"form": form})


# UPDATE
def cancel_reason_update(request, pk):
    reason = get_object_or_404(CancelReason, pk=pk)
    form = CancelReasonForm(request.POST or None, instance=reason)
    if form.is_valid():
        form.save()
        return redirect("cancel_reason_list")
    return render(request, "superadmin/cancel_reason/form.html", {"form": form})


# DELETE
def cancel_reason_delete(request, pk):
    reason = get_object_or_404(CancelReason, pk=pk)

    if request.method == "POST":
        reason.delete()

    return redirect("cancel_reason_list")





# LIST
def things_list(request):
    query = request.GET.get("q", "")
    things = Thingstocarry.objects.all()

    if query:
        things = things.filter(name__icontains=query)

    return render(request, "superadmin/thingstocarry/list.html", {
        "things": things,
        "query": query
    })


# CREATE
def things_create(request):
    form = ThingstocarryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("things_list")

    return render(request, "superadmin/thingstocarry/form.html", {"form": form})


# UPDATE
def things_update(request, pk):
    obj = get_object_or_404(Thingstocarry, pk=pk)
    form = ThingstocarryForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect("things_list")

    return render(request, "superadmin/thingstocarry/form.html", {"form": form})


# DELETE
def things_delete(request, pk):
    obj = get_object_or_404(Thingstocarry, pk=pk)

    if request.method == "POST":
        obj.delete()
        return redirect("things_list")

    return redirect("things_list")



# from django.db.models import Q


# LIST + SEARCH
def propertyrules_list(request):
    query = request.GET.get("q", "")
    rules = Propertyrules.objects.all()

    if query:
        rules = rules.filter(name__icontains=query)

    return render(request, "superadmin/propertyrules/list.html", {
        "rules": rules,
        "query": query
    })


# CREATE
def propertyrules_create(request):
    form = PropertyrulesForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("propertyrules_list")

    return render(request, "superadmin/propertyrules/form.html", {"form": form})


# UPDATE
def propertyrules_update(request, pk):
    obj = get_object_or_404(Propertyrules, pk=pk)
    form = PropertyrulesForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect("propertyrules_list")

    return render(request, "superadmin/propertyrules/form.html", {"form": form})


# DELETE
def propertyrules_delete(request, pk):
    obj = get_object_or_404(Propertyrules, pk=pk)

    if request.method == "POST":
        obj.delete()

    return redirect("propertyrules_list")










from cms.models import PageSEO


# 🔹 List
def seo_list(request):
    query = request.GET.get("q", "")

    seo_pages = PageSEO.objects.all()

    if query:
        seo_pages = seo_pages.filter(
            Q(page__icontains=query) |
            Q(meta_title__icontains=query) |
            Q(meta_description__icontains=query)
        )

    context = {
        "seo_pages": seo_pages,
        "query": query,
    }

    return render(request, "superadmin/seo/seo_list.html", context)

# 🔹 Create
def seo_create(request):
    form = PageSEOForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("seo_list")
    return render(request, "superadmin/seo/seo_form.html", {"form": form})


# 🔹 Update
def seo_update(request, pk):
    seo = get_object_or_404(PageSEO, pk=pk)
    form = PageSEOForm(request.POST or None, instance=seo)
    if form.is_valid():
        form.save()
        return redirect("seo_list")
    return render(request, "superadmin/seo/seo_form.html", {"form": form})


# 🔹 Delete
def seo_delete(request, pk):
    seo = get_object_or_404(PageSEO, pk=pk)
    seo.delete()
    return redirect("seo_list")