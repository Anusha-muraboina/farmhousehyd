"""
URL configuration for farmhousehyd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static


from django.views.generic import TemplateView


from django.contrib.sitemaps.views import sitemap

from farmhousehyd.sitemap import StaticSitemap, FarmhouseSitemap, BlogSitemap

sitemaps = {
    "static": StaticSitemap(),
    "farmhouses": FarmhouseSitemap(),
    "blogs": BlogSitemap(),
}
# from farmhousehyd.sitemap import BlogSitemap, BlogListSitemap,StaticSitemap,BookingSitemap

# sitemaps = {
#     "blogs": BlogSitemap(),
#     "blog-list": BlogListSitemap(),
#     "static": StaticSitemap(),
#     "bookings": BookingSitemap(),
# }


urlpatterns = [
    
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
    ),
    
    path('admin/', admin.site.urls),
    path('farmhouse_admin/' , include("farmhouse_owner.urls")),
    path('farmhouse_superadmin/' , include("superadmin_dashboard.urls")),
    path('accounts/' , include("accounts.urls")),
    path('', include('farmhouse.urls')),
    path('contact/',include('contact.urls')),
    path('user/',include('user.urls')),
    path('blogs/',include('blogs.urls')),
    path('bookings/',include('booking.urls')),
    path('coupon/',include('coupon.urls')),
    path('rating/',include('rating.urls')),
    path('cms/',include('cms.urls')),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    
        # ✅ ADD THIS LINE
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path('api-auth/', include('rest_framework.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
