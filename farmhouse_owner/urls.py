from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login_view, name="owner_login"),
    path("dashboard/", owner_dashboard, name="owner_dashboard"),
    # path('farmhouse/',owner_farmhouses ,name = "owner_farmhouses"),
    
    path("logout/", owner_logout, name="owner_logout"),
    
    
      # FARMHOUSE CRUD
    path("farmhouses/", owner_farmhouses, name="owner_farmhouses"),

    path("farmhouses/add/",
         add_farmhouse,
         name="owner_farmhouse_add"),

    path("farmhouses/edit/<int:id>/",
         edit_farmhouse,
         name="owner_farmhouse_edit"),

    path("farmhouses/delete/<int:id>/",
         delete_farmhouse,
         name="owner_farmhouse_delete"),
    
    path(
        "bookings/",
        owner_booking_list,
        name="owner_bookings"
    ),

    path( "booking/<int:pk>/",owner_booking_detail, name="owner_booking_detail"),
    
    path("owner/bookings/create/", owner_booking_create,  name="owner-booking-create"),
    path("owner/bookings/<int:pk>/edit/",owner_booking_update,name="owner-booking-update"),
    path( "owner/bookings/<int:pk>/cancel/", owner_booking_cancel, name="owner-booking-cancel"),
    
    path("owner/bookings/lists/", owner_booking_list_api ,name="owner_booking_list_api"),
    path("owner/bookings/detail/<int:pk>/", owner_booking_detail_api ,name="owner_booking_detail_api"),
    path(
    "owner/bookings/<int:pk>/update/",
    owner_booking_update_api,
    name="owner_booking_update_api"
    ),
    
    path( "messages/", owner_contact_list, name="owner_contact_list"),

    path("messages/<int:pk>/", owner_contact_detail, name="owner_contact_detail"),

    path("coupons/", owner_coupon_list, name="owner_coupon_list"),

    path("coupons/add/",owner_coupon_create,name="owner_coupon_create"),

    path( "coupons/<int:pk>/edit/",owner_coupon_update, name="owner_coupon_update"),


    path(
        "coupons/<int:pk>/delete/",
        owner_coupon_delete,
        name="owner_coupon_delete"
    ),
    
    
    path(
    "blocked-dates/",
    owner_blocked_dates_list,
    name="owner_blocked-dates"
    ),

    path(
        "blocked-dates/create/",
        owner_blocked_dates_create,
        name="owner_blocked-dates-create"
    ),

    path(
        "blocked-dates/<int:pk>/edit/",
        owner_blocked_dates_update,
        name="owner_blocked-dates-update"
    ),

    path(
        "blocked-dates/<int:pk>/delete/",
        owner_blocked_dates_delete,
        name="owner_blocked-dates-delete"
    ),
    
    path(
        "blocked-ranges/",
        owner_blocked_ranges,
        name="owner-blocked-ranges"
    ),
    
    # urls.py

    path("owner_payment-policies/", owner_payment_policy_list, name="owner_payment_policy_list"),
    path("owner_payment-policies/add/", owner_payment_policy_create, name="owner_payment_policy_create"),
    path("owner_payment-policies/<int:pk>/edit/", owner_payment_policy_update, name="owner_payment_policy_update"),
    path("owner_payment-policies/<int:pk>/delete/", owner_payment_policy_delete, name="owner_payment_policy_delete"),


    path("admin/calc-booking-price/", owner_calculate_booking_price,  name="owner_calc_booking_price" ),
    path( "owner/invoice/<str:booking_id>/", owner_view_invoice, name="owner_view_invoice"),
    
    
    path("offers/", owner_offer_list, name="owner_offer_list"),
    path("offers/add/", owner_offer_create, name="owner_offer_create"),
    path("offers/<int:pk>/edit/", owner_offer_update, name="owner_offer_update"),
    path("offers/<int:pk>/delete/", owner_offer_delete, name="owner_offer_delete"),
    
    
    path(
    "booking/send-coupon/<int:booking_id>/",
        send_booking_coupon,
        name="send_booking_coupon"
    ),
     
    path("download/<int:coupon_id>/", download_coupon, name="download_coupon"),
        
    # urls.py






    # # OWNER
    # path(
    #     "owner/farmhouse/<int:pk>/calendar/",
    #     owner_farmhouse_calendar,
    #     name="owner_farmhouse_calendar"
    # ),

    # # PUBLIC SHARE
    # path(
    #     "calendar/<slug:slug>/",
    #     public_calendar,
    #     name="public_calendar"
    # ),

    # # API (IMPORTANT)
    # path(
    #     "bookings/blocked-dates/<slug:slug>/",
    #     get_blocked_dates,
    #     name="blocked_dates"
    # ),











]
