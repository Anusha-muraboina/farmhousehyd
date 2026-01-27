from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.superadmin_login, name="superadmin-login"),
    path("logout/", views.superadmin_logout, name="superadmin-logout"),

    path("dashboard/", views.superadmin_dashboard, name="superadmin-dashboard"),
    # path("farmhouses/", views.all_farmhouses, name="superadmin-farmhouses"),
    
    path("farmhouses/", views.farmhouse_list, name="superadmin-farmhouses"),
    path("farmhouses/add/", views.farmhouse_add, name="superadmin-farmhouse-add"),
    path("farmhouses/edit/<int:id>/", views.farmhouse_edit, name="superadmin-farmhouse-edit"),
    path("farmhouses/delete/<int:id>/", views.farmhouse_delete, name="superadmin-farmhouse-delete"),
    
    
    path("banners/", views.banner_list, name="banner-list"),
    path("banners/add/", views.banner_create, name="banner-add"),
    path("banners/<int:pk>/edit/", views.banner_update, name="banner-edit"),
    path("banners/<int:pk>/delete/", views.banner_delete, name="banner-delete"),

    # Locations
    path("locations/", views.location_list, name="location-list"),
    path("locations/add/", views.location_create, name="location-add"),
    path("locations/<int:pk>/edit/", views.location_update, name="location-edit"),
    path("locations/<int:pk>/delete/", views.location_delete, name="location-delete"),

    # Amenities
    path("amenities/", views.amenity_list, name="amenity-list"),
    path("amenities/add/", views.amenity_create, name="amenity-add"),
    path("amenities/<int:pk>/edit/", views.amenity_update, name="amenity-edit"),
    path("amenities/<int:pk>/delete/", views.amenity_delete, name="amenity-delete"),
]
