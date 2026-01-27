from django.shortcuts import render

# Create your views here.
# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
def superadmin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_superuser
    )(view_func)

def superadmin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect("superadmin-dashboard")

        messages.error(request, "Invalid credentials or not Super Admin")

    return render(request, "superadmin/login.html")
def superadmin_logout(request):
    logout(request)
    return redirect("superadmin-login")



from farmhouse.models import Farmhouse
from django.contrib.auth import get_user_model

User = get_user_model()

@superadmin_required
def superadmin_dashboard(request):
    context = {
        "total_users": User.objects.count(),
        "total_farmhouses": Farmhouse.objects.count(),
        "active_farmhouses": Farmhouse.objects.filter(is_active=True).count(),
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


def superadmin_required(user):
    return user.is_superuser


# ===============================
# LIST
# ===============================
@login_required
@user_passes_test(superadmin_required)
def farmhouse_list(request):
    farmhouses = Farmhouse.objects.all()
    return render(
        request,
        "superadmin/farmhouses.html",
        {"farmhouses": farmhouses}
    )


# ===============================
# ADD
# ===============================
def farmhouse_add(request):
    if request.method == "POST":
        form = FarmhouseForm(request.POST)
        pricing_form = FarmhousePricingForm(request.POST)

        if form.is_valid() and pricing_form.is_valid():
            farmhouse = form.save(commit=False)
            farmhouse.user = request.user
            farmhouse.save()
            form.save_m2m()

            pricing = pricing_form.save(commit=False)
            pricing.farmhouse = farmhouse
            pricing.save()

            return redirect("superadmin-farmhouses")

    else:
        form = FarmhouseForm()
        pricing_form = FarmhousePricingForm()
        farmhouse_gallery = FarmhouseImageForm()

    return render(request, "superadmin/farmhouse_add.html", {
        "form": form,
        "pricing_form": pricing_form,
        "farmhouse_gallery":farmhouse_gallery
    })


# ===============================
# EDIT
# ===============================
@login_required
@user_passes_test(superadmin_required)
def farmhouse_edit(request, id):

    farmhouse = get_object_or_404(Farmhouse, id=id)
    pricing, _ = FarmhousePricing.objects.get_or_create(farmhouse=farmhouse)

    if request.method == "POST":
        form = FarmhouseForm(request.POST, instance=farmhouse)
        pricing_form = FarmhousePricingForm(
            request.POST,
            instance=pricing
        )

        if form.is_valid() and pricing_form.is_valid():
            form.save()
            pricing_form.save()
            return redirect("superadmin-farmhouses")

    else:
        form = FarmhouseForm(instance=farmhouse)
        pricing_form = FarmhousePricingForm(instance=pricing)

    return render(
        request,
        "superadmin/farmhouse_edit.html",
        {
            "form": form,
            "pricing_form": pricing_form,
            "farmhouse": farmhouse
        }
    )


# ===============================
# DELETE
# ===============================
@login_required
@user_passes_test(superadmin_required)
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
def banner_list(request):
    items = Banner.objects.all()

    return render(request, "superadmin/banners/banner_list.html", {
        "items": items,
        "title": "Banners",
        "add_url": "banner_add",   # ✅ URL name
    })


def banner_create(request):
    form = BannerForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("banner-list")
    return render(request, "superadmin/banners/banner_form.html", {"form": form})


def banner_update(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    form = BannerForm(request.POST or None, request.FILES or None, instance=banner)
    if form.is_valid():
        form.save()
        return redirect("banner-list")
    return render(request, "superadmin/banners/banner_form.html", {"form": form})


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
def location_list(request):
    items = Location.objects.all()
    return render(request, "superadmin/locations/location_list.html", {
        "items": items,
        "title": "Locations",
        "add_url": "location-add",
    })


def location_create(request):
    form = LocationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("location-list")
    return render(request, "superadmin/locations/location_form.html", {"form": form})


def location_update(request, pk):
    obj = get_object_or_404(Location, pk=pk)
    form = LocationForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("location-list")
    return render(request, "superadmin/locations/location_form.html", {"form": form})


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


def amenity_list(request):
    items = Amenity.objects.all()
    return render(request, "superadmin/amenities/amenities_list.html", {
        "items": items,
        "title": "Amenities",
        "add_url": "amenity-add",
    })


def amenity_create(request):
    form = AmenityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("amenity-list")
    return render(request, "superadmin/amenities/amenities_form.html", {"form": form})


def amenity_update(request, pk):
    obj = get_object_or_404(Amenity, pk=pk)
    form = AmenityForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("amenity-list")
    return render(request, "superadmin/amenities/amenities_form.html", {"form": form})


def amenity_delete(request, pk):
    obj = get_object_or_404(Amenity, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("amenity-list")
    # return render(request, "superadmin/amenities/amenities_delete.html", {"obj": obj})

