from django.urls import path
from . import views
from .views import CreateBookingAPI, razorpay_webhook ,blocked_dates_api ,BookingSuccessAPI ,booking_success_page

urlpatterns = [
    # BOOKINGS
    path("create/", CreateBookingAPI.as_view(), name="create_booking"),

    # RAZORPAY
    path("payments/webhook/", razorpay_webhook, name="razorpay_webhook"),
    
    # booking/urls.py

    # path(
    # 'api/blocked-dates/<int:farmhouse_id>/',
    # blocked_dates_api
    # ),
    path('blocked-dates/<int:farmhouse_id>/', blocked_dates_api),
    # path( "/api/booking-success/<str:booking_id>/", BookingSuccessAPI.as_view()),
    path(
        "api/booking-success/<int:booking_id>/",
        BookingSuccessAPI.as_view(),
        name="booking-success-api"
    ),

    path(
        "booking-success/<int:booking_id>/",
        booking_success_page,  name="booking_success"
    ),



]


# urlpatterns = [

    # ==========================
    # FARMHOUSE DETAIL + BOOKING
    # ==========================
    # path(
    #     "farmhouse/<slug:slug>/",
    #     views.farmhouse_detail,
    #     name="farmhouse_detail"
    # ),

    # # ==========================
    # # BOOKING CONFIRMATION
    # # ==========================
    # path(
    #     "booking/confirmation/<str:booking_id>/",
    #     views.booking_confirmation,
    #     name="booking_confirmation"
    # ),

    # # ==========================
    # # COUPON (AJAX)
    # # ==========================
    # path(
    #     "coupon/validate/",
    #     views.validate_coupon,
    #     name="validate_coupon"
    # ),

    # # ==========================
    # # RAZORPAY
    # # ==========================
    # path(
    #     "payment/verify/",
    #     views.verify_razorpay_payment,
    #     name="verify_razorpay_payment"
    # ),
    
    
    
    
    
    
# ]
