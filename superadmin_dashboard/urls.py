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
    
    
        # CATEGORY
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_add, name="category_add"),
    path("categories/edit/<int:pk>/", views.category_edit, name="category_edit"),
    path("categories/delete/<int:pk>/", views.category_delete, name="category_delete"),

    # TAGS
    path("tags/", views.tag_list, name="tag_list"),
    path("tags/add/", views.tag_add, name="tag_add"),
    path("tags/edit/<int:pk>/", views.tag_edit, name="tag_edit"),
    path("tags/delete/<int:pk>/", views.tag_delete, name="tag_delete"),

    # BLOG
    path("blogs/", views.blog_list, name="blog_lists"),
    path("blogs/add/", views.blog_add, name="blog_add"),
    path("blogs/edit/<int:pk>/", views.blog_edit, name="blog_edit"),
    path("blogs/delete/<int:pk>/", views.blog_delete, name="blog_delete"),

    # COMMENTS
    path("comments/", views.comment_list, name="comment_list"),
    path("comments/toggle/<int:pk>/", views.comment_toggle, name="comment_toggle"),
    
    
    # cms
    # Choose Services
    path("choose-services/", views.choose_services_list, name="choose_services_list"),
    path("choose-services/add/", views.choose_services_add, name="choose_services_add"),
    path("choose-services/edit/<int:id>/", views.choose_services_edit, name="choose_services_edit"),
    path("choose-services/delete/<int:id>/", views.choose_services_delete, name="choose_services_delete"),

    # Facilities
    path("facilities/", views.facilities_list, name="facilities_list"),
    path("facilities/add/", views.facilities_add, name="facilities_add"),
    path("facilities/edit/<int:id>/", views.facilities_edit, name="facilities_edit"),
    path("facilities/delete/<int:id>/", views.facilities_delete, name="facilities_delete"),

    # Our Facility
    path("our-facility/", views.our_facility_list, name="our_facility_list"),
    path("our-facility/add/", views.our_facility_add, name="our_facility_add"),
    path("our-facility/edit/<int:id>/", views.our_facility_edit, name="our_facility_edit"),
    path("our-facility/delete/<int:id>/", views.our_facility_delete, name="our_facility_delete"),

    # Who We Are
    path("who-we-are/", views.who_we_are_list, name="who_we_are_list"),
    path("who-we-are/add/", views.who_we_are_add, name="who_we_are_add"),
    path("who-we-are/edit/<int:id>/", views.who_we_are_edit, name="who_we_are_edit"),
    path("who-we-are/delete/<int:id>/", views.who_we_are_delete, name="who_we_are_delete"),

    # About Section
    path("about-section/", views.about_section_list, name="about_section_list"),
    path("about-section/add/", views.about_section_add, name="about_section_add"),
    path("about-section/edit/<int:id>/", views.about_section_edit, name="about_section_edit"),
    path("about-section/delete/<int:id>/", views.about_section_delete, name="about_section_delete"),

    # About Feature
    path("about-feature/", views.about_feature_list, name="about_feature_list"),
    path("about-feature/add/", views.about_feature_add, name="about_feature_add"),
    path("about-feature/edit/<int:id>/", views.about_feature_edit, name="about_feature_edit"),
    path("about-feature/delete/<int:id>/", views.about_feature_delete, name="about_feature_delete"),

    # About Who We Are
    path("about-who-we-are/", views.about_who_we_are_list, name="about_who_we_are_list"),
    path("about-who-we-are/add/", views.about_who_we_are_add, name="about_who_we_are_add"),
    path("about-who-we-are/edit/<int:id>/", views.about_who_we_are_edit, name="about_who_we_are_edit"),
    path("about-who-we-are/delete/<int:id>/", views.about_who_we_are_delete, name="about_who_we_are_delete"),
    
    
    
    path("coupons/", views.coupon_list, name="coupon_list"),
    path("coupons/add/", views.coupon_add, name="coupon_add"),
    path("coupons/edit/<int:id>/", views.coupon_edit, name="coupon_edit"),
    path("coupons/delete/<int:id>/", views.coupon_delete, name="coupon_delete"),

    path("coupon-usage/", views.coupon_usage_list, name="coupon_usage_list"),

]
