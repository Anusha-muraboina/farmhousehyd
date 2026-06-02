from django.urls import path
from . import views
from .views import admin_send_booking_coupon,download_coupon
urlpatterns = [

    path("dashboard/", views.superadmin_dashboard, name="superadmin-dashboard"),
    # path("farmhouses/", views.all_farmhouses, name="superadmin-farmhouses"),

    path("farmhouses/", views.farmhouse_list, name="superadmin-farmhouses"),
    path("farmhouses/add/", views.farmhouse_add, name="superadmin-farmhouse-add"),
    path("farmhouses/edit/<int:id>/", views.farmhouse_edit, name="superadmin-farmhouse-edit"),
    path("farmhouses/delete/<int:id>/", views.farmhouse_delete, name="superadmin-farmhouse-delete"),
    path('delete-image/<int:id>/', views.delete_farmhouse_image, name='delete_farmhouse_image'),
#   # 🗑 Trash Page
#     path('farmhouses/trash/', views.farmhouse_trash, name='farmhouse-trash'),

#     # ♻️ Restore
#     path('farmhouses/restore/<int:id>/', views.farmhouse_restore, name='farmhouse-restore'),

#     # ❌ Permanent Delete
#     path('farmhouses/delete-permanent/<int:id>/', views.farmhouse_delete_permanent, name='farmhouse-delete-permanent'),
    
    
    
    path("trash/", views.farmhouse_trash, name="farmhouse-trash"),
    path("verify-trash-pin/", views.verify_trash_pin, name="verify-trash-pin"),
    path("restore/<int:id>/", views.farmhouse_restore, name="farmhouse-restore"),
    path("delete-permanent/<int:id>/", views.farmhouse_delete_permanent, name="farmhouse-delete-permanent"),
    
    
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

    path("users/", views.admin_user_list, name="admin_user_list"),
    path('users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path("users/add/", views.admin_user_add, name="admin_user_add"),
    path("users/edit/<int:id>/", views.admin_user_edit, name="admin_user_edit"),
    path("users/delete/<int:id>/", views.admin_user_delete, name="admin_user_delete"),
    
    path("info/", views.contact_info_list, name="contact_info_list"),
    path("info/add/", views.contact_info_add, name="contact_info_add"),
    path("info/edit/<int:id>/", views.contact_info_edit, name="contact_info_edit"),
    path("info/delete/<int:id>/", views.contact_info_delete, name="contact_info_delete"),

    path("messages/", views.contact_message_list, name="contact_message_list"),
    path("messages/delete/<int:id>/", views.contact_message_delete, name="contact_message_delete"),
    
    path("payment-policies/", views.payment_policy_list, name="payment_policy_list"),
    path("payment-policies/add/", views.payment_policy_create, name="payment_policy_create"),
    path("payment-policies/<int:pk>/edit/", views.payment_policy_update, name="payment_policy_update"),
    path( "payment-policy/<int:pk>/delete/",views.payment_policy_delete,  name="payment_policy_delete" ),


# urls.py

    path("farmhouse-facilities/", views.facility_list, name="farmhouse-facility-list"),
    path("farmhouse-facilities/add/", views.facility_create, name="farmhouse-facility-create"),
    path("farmhouse-facilities/<int:pk>/edit/", views.facility_update, name="farmhouse-facility-update"),
    path("farmhouse-facilities/<int:pk>/delete/", views.facility_delete, name="farmhouse-facility-delete"),


    path("admin/calc-booking-price/", views.admin_calculate_booking_price,  name="admin_calc_booking_price" ),
    
    
    path("admin/bookings/",  views.admin_booking_list, name="admin-bookings"),
    path("admin/bookings/create/", views.admin_booking_create,  name="admin-booking-create"),
    path("admin/bookings/<int:pk>/",views.admin_booking_detail,name="admin-booking-detail"),
    path("admin/bookings/<int:pk>/edit/",views.admin_booking_update,name="admin-booking-update"),
    path( "admin/bookings/<int:pk>/cancel/", views.admin_booking_cancel, name="admin-booking-cancel"),
    
    # path("admin/blocked-dates/",views.blocked_dates_list,name="blocked-dates"),
    # path( "admin/blocked-dates/create/", views.blocked_dates_create, name="blocked-dates-create"),
    # path("admin/blocked-dates/<int:pk>/edit/",views.blocked_dates_update,name="blocked-dates-update"),
    # path("admin/blocked-dates/<int:pk>/delete/",views.blocked_dates_delete,name="blocked-dates-delete"),
    
    path("admin/blocked-dates/",views.blocked_dates_list,name="blocked-dates"),
    path( "admin/blocked-dates/create/", views.blocked_dates_create, name="blocked-dates-create" ),
    path( "admin/blocked-dates/<int:pk>/edit/",views.blocked_dates_update, name="blocked-dates-update"),
    path("admin/blocked-dates/<int:pk>/delete/",views.blocked_dates_delete,name="blocked-dates-delete"),

    path("cancel-reasons/", views.cancel_reason_list, name="cancel_reason_list"),
    path("cancel-reasons/add/", views.cancel_reason_create, name="cancel_reason_create"),
    path("cancel-reasons/<int:pk>/edit/", views.cancel_reason_update, name="cancel_reason_update"),
    path("cancel-reasons/<int:pk>/delete/", views.cancel_reason_delete, name="cancel_reason_delete"),


    path("things/", views.things_list, name="things_list"),
    path("things/add/", views.things_create, name="things_create"),
    path("things/<int:pk>/edit/", views.things_update, name="things_update"),
    path("things/<int:pk>/delete/", views.things_delete, name="things_delete"),

    path("property-rules/", views.propertyrules_list, name="propertyrules_list"),
    path("property-rules/add/", views.propertyrules_create, name="propertyrules_create"),
    path("property-rules/<int:pk>/edit/", views.propertyrules_update, name="propertyrules_update"),
    path("property-rules/<int:pk>/delete/", views.propertyrules_delete, name="propertyrules_delete"),
    
    
    # path("seo/", views.seo_list, name="seo_list"),
    # path("seo/create/", views.seo_create, name="seo_create"),
    # path("seo/<int:pk>/edit/", views.seo_update, name="seo_update"),
    # path("seo/<int:pk>/delete/", views.seo_delete, name="seo_delete"),
    
    
    path("seo/", views.seo_list, name="seo_list"),
    path("seo/create/", views.seo_create, name="seo_create"),
    path("seo/<int:pk>/edit/", views.seo_update, name="seo_update"),
    path("seo/<int:pk>/delete/", views.seo_delete, name="seo_delete"),


    path( "admin/invoice/<str:booking_id>/", views.admin_view_invoice, name="admin_view_invoice"),
    
    
    path("popup/", views.popup_list, name="popup-list"),
    path("popup/create/", views.popup_create, name="popup-create"),
    path("popup/<int:pk>/edit/", views.popup_update, name="popup-update"),
    path("popup/<int:pk>/delete/", views.popup_delete, name="popup-delete"),
    
    
    path("wallets/", views.wallet_list, name="wallet_list"),
    path("wallets/create/", views.wallet_create, name="wallet_create"),
    path("wallets/<int:pk>/edit/", views.wallet_update, name="wallet_update"),
    path("wallets/<int:pk>/delete/", views.wallet_delete, name="wallet_delete"),
    
    
    
    path("admin_offers/", views.admin_offer_list, name="admin_offer_list"),
    path("admin_offers/add/", views.admin_offer_create, name="admin_offer_create"),
    path("admin_offers/<int:pk>/edit/", views.admin_offer_update, name="admin_offer_update"),
    path("admin_offers/<int:pk>/delete/", views.admin_offer_delete, name="admin_offer_delete"),
    
    
    # path("booking/admin_send-coupon/<int:booking_id>/",admin_send_booking_coupon,name="admin_send_booking_coupon" ),
    path(
    "send-coupon/<int:booking_id>/",
        admin_send_booking_coupon,
        name="admin_send_booking_coupon"
    ),
    
    path("download/<int:coupon_id>/", download_coupon, name="download_coupon"),
     
    

    # OWNER
    # path(
    #     "admin/farmhouse/<int:pk>/calendar/",
    #     views.superadmin_farmhouse_calendar,
    #     name="owner_farmhouse_calendar"
    # ),

    # PUBLIC SHARE
    # path(
    #     "calendar/<slug:slug>/",
    #     views.superadmin_public_calendar,
    #     name="public_calendar"
    # ),

    # # API (IMPORTANT)
    # path(
    #     "bookings/blocked-dates/<slug:slug>/",
    #     views.superadmin_get_blocked_dates,
    #     name="blocked_dates"
    # ),


    path(
    "ratings/",
    views.admin_rating_list,
    name="admin_rating_list"
    ),

    path(
        "ratings/add/",
        views.admin_rating_add,
        name="admin_rating_add"
    ),

    path(
        "ratings/edit/<int:id>/",
        views.admin_rating_edit,
        name="admin_rating_edit"
    ),

    path(
        "ratings/delete/<int:id>/",
        views.admin_rating_delete,
        name="admin_rating_delete"
    ),


]
