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



@login_required
@user_passes_test(superadmin_required)
def category_list(request):
    categories = BlogCategory.objects.all()
    return render(request, "superadmin/blog/category_list.html", {
        "categories": categories
    })


@login_required
@user_passes_test(superadmin_required)
def category_add(request):
    if request.method == "POST":
        BlogCategory.objects.create(
            name=request.POST.get("name"),
            is_active=True if request.POST.get("is_active") else False
        )
        messages.success(request, "Category added successfully")
        return redirect("category_list")

    return render(request, "superadmin/blog/category_form.html")


@login_required
@user_passes_test(superadmin_required)
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


@login_required
@user_passes_test(superadmin_required)
def category_delete(request, pk):
    BlogCategory.objects.filter(pk=pk).delete()
    messages.success(request, "Category deleted")
    return redirect("category_list")


# ===============================
# TAG CRUD
# ===============================

@login_required
@user_passes_test(superadmin_required)
def tag_list(request):
    tags = BlogTag.objects.all()
    return render(request, "superadmin/blog/tag_list.html", {"tags": tags})


@login_required
@user_passes_test(superadmin_required)
def tag_add(request):
    if request.method == "POST":
        BlogTag.objects.create(
            name=request.POST.get("name")
        )
        messages.success(request, "Tag added")
        return redirect("tag_list")

    return render(request, "superadmin/blog/tag_form.html")


@login_required
@user_passes_test(superadmin_required)
def tag_edit(request, pk):
    tag = get_object_or_404(BlogTag, pk=pk)

    if request.method == "POST":
        tag.name = request.POST.get("name")
        tag.save()
        messages.success(request, "Tag updated")
        return redirect("tag_list")

    return render(request, "superadmin/blog/tag_form.html", {"tag": tag})


@login_required
@user_passes_test(superadmin_required)
def tag_delete(request, pk):
    BlogTag.objects.filter(pk=pk).delete()
    messages.success(request, "Tag deleted")
    return redirect("tag_list")


# ===============================
# BLOG CRUD
# ===============================

@login_required
@user_passes_test(superadmin_required)
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, "superadmin/blog/blog_list.html", {
        "blogs": blogs
    })


@login_required
@user_passes_test(superadmin_required)
def blog_add(request):
    categories = BlogCategory.objects.filter(is_active=True)
    tags = BlogTag.objects.all()

    if request.method == "POST":
        blog = Blog.objects.create(
            title=request.POST.get("title"),
            category_id=request.POST.get("category"),
            short_description=request.POST.get("short_description"),
            content=request.POST.get("content"),
            read_time=request.POST.get("read_time"),
            is_published=True if request.POST.get("is_published") else False,
        )

        if request.FILES.get("image"):
            blog.image = request.FILES.get("image")
            blog.save()

        tag_ids = request.POST.getlist("tags")
        blog.tags.set(tag_ids)

        messages.success(request, "Blog created successfully")
        return redirect("blog_list")

    return render(request, "superadmin/blog/blog_form.html", {
        "categories": categories,
        "tags": tags
    })


@login_required
@user_passes_test(superadmin_required)
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    categories = BlogCategory.objects.filter(is_active=True)
    tags = BlogTag.objects.all()

    if request.method == "POST":
        blog.title = request.POST.get("title")
        blog.category_id = request.POST.get("category")
        blog.short_description = request.POST.get("short_description")
        blog.content = request.POST.get("content")
        blog.read_time = request.POST.get("read_time")
        blog.is_published = True if request.POST.get("is_published") else False

        if request.FILES.get("image"):
            blog.image = request.FILES.get("image")

        blog.save()
        blog.tags.set(request.POST.getlist("tags"))

        messages.success(request, "Blog updated successfully")
        return redirect("blog_list")

    return render(request, "superadmin/blog/blog_form.html", {
        "blog": blog,
        "categories": categories,
        "tags": tags
    })


@login_required
@user_passes_test(superadmin_required)
def blog_delete(request, pk):
    Blog.objects.filter(pk=pk).delete()
    messages.success(request, "Blog deleted")
    return redirect("blog_list")


# ===============================
# COMMENTS MODERATION
# ===============================

@login_required
@user_passes_test(superadmin_required)
def comment_list(request):
    comments = BlogComment.objects.select_related("blog").order_by("-created_at")
    return render(request, "superadmin/blog/comment_list.html", {
        "comments": comments
    })


@login_required
@user_passes_test(superadmin_required)
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

def choose_services_list(request):
    services = paginate(request, Choos_Services.objects.all())
    return render(request, "cms/choose_services_list.html", {"services": services})


def choose_services_add(request):
    form = ChooseServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Service added successfully")
        return redirect("choose_services_list")
    return render(request, "cms/choose_services_form.html", {"form": form})


def choose_services_edit(request, id):
    obj = get_object_or_404(Choos_Services, id=id)
    form = ChooseServiceForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Service updated successfully")
        return redirect("choose_services_list")
    return render(request, "cms/choose_services_form.html", {"form": form})


def choose_services_delete(request, id):
    get_object_or_404(Choos_Services, id=id).delete()
    messages.success(request, "Deleted successfully")
    return redirect("choose_services_list")


# ================= FACILITIES =================
def facilities_list(request):
    facilities = paginate(request, Facilities.objects.all())
    return render(request, "cms/facilities_list.html", {"facilities": facilities})


def facilities_add(request):
    form = FacilityForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Facility added")
        return redirect("facilities_list")
    return render(request, "cms/facilities_form.html", {"form": form})


def facilities_edit(request, id):
    obj = get_object_or_404(Facilities, id=id)
    form = FacilityForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Facility updated")
        return redirect("facilities_list")
    return render(request, "cms/facilities_form.html", {"form": form})


def facilities_delete(request, id):
    get_object_or_404(Facilities, id=id).delete()
    messages.success(request, "Deleted successfully")
    return redirect("facilities_list")


# ================= OUR FACILITY =================
def our_facility_list(request):
    items = paginate(request, OurFacility.objects.all())
    return render(request, "cms/our_facility_list.html", {"items": items})


def our_facility_add(request):
    form = OurFacilityForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Facility added")
        return redirect("our_facility_list")
    return render(request, "cms/our_facility_form.html", {"form": form})


def our_facility_edit(request, id):
    obj = get_object_or_404(OurFacility, id=id)
    form = OurFacilityForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated successfully")
        return redirect("our_facility_list")
    return render(request, "cms/our_facility_form.html", {"form": form})


def our_facility_delete(request, id):
    get_object_or_404(OurFacility, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("our_facility_list")


# ================= WHO WE ARE =================
def who_we_are_list(request):
    items = paginate(request, WhoWeAre.objects.all())
    return render(request, "cms/who_we_are_list.html", {"items": items})


def who_we_are_add(request):
    form = WhoWeAreForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Added")
        return redirect("who_we_are_list")
    return render(request, "cms/who_we_are_form.html", {"form": form})


def who_we_are_edit(request, id):
    obj = get_object_or_404(WhoWeAre, id=id)
    form = WhoWeAreForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect("who_we_are_list")
    return render(request, "cms/who_we_are_form.html", {"form": form})


def who_we_are_delete(request, id):
    get_object_or_404(WhoWeAre, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("who_we_are_list")


# ================= ABOUT SECTION =================
def about_section_list(request):
    items = paginate(request, AboutSection.objects.all())
    return render(request, "cms/about_section_list.html", {"items": items})


def about_section_add(request):
    form = AboutSectionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Saved")
        return redirect("about_section_list")
    return render(request, "cms/about_section_form.html", {"form": form})


def about_section_edit(request, id):
    obj = get_object_or_404(AboutSection, id=id)
    form = AboutSectionForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect("about_section_list")
    return render(request, "cms/about_section_form.html", {"form": form})


def about_section_delete(request, id):
    get_object_or_404(AboutSection, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("about_section_list")


# ================= ABOUT FEATURE =================
def about_feature_list(request):
    items = paginate(request, AboutFeature.objects.all())
    return render(request, "cms/about_feature_list.html", {"items": items})


def about_feature_add(request):
    form = AboutFeatureForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Added")
        return redirect("about_feature_list")
    return render(request, "cms/about_feature_form.html", {"form": form})


def about_feature_edit(request, id):
    obj = get_object_or_404(AboutFeature, id=id)
    form = AboutFeatureForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect("about_feature_list")
    return render(request, "cms/about_feature_form.html", {"form": form})


def about_feature_delete(request, id):
    get_object_or_404(AboutFeature, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("about_feature_list")


# ================= ABOUT WHO WE ARE =================
def about_who_we_are_list(request):
    items = paginate(request, AboutWhoWeAre.objects.all())
    return render(request, "cms/about_who_we_are_list.html", {"items": items})


def about_who_we_are_add(request):
    form = AboutWhoWeAreForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Saved")
        return redirect("about_who_we_are_list")
    return render(request, "cms/about_who_we_are_form.html", {"form": form})


def about_who_we_are_edit(request, id):
    obj = get_object_or_404(AboutWhoWeAre, id=id)
    form = AboutWhoWeAreForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect("about_who_we_are_list")
    return render(request, "cms/about_who_we_are_form.html", {"form": form})


def about_who_we_are_delete(request, id):
    get_object_or_404(AboutWhoWeAre, id=id).delete()
    messages.success(request, "Deleted")
    return redirect("about_who_we_are_list")
