from django.urls import path
from . import views
from .views import CreateBookingAPI,CancelReasonListAPI, razorpay_webhook ,blocked_dates_api ,BookingSuccessAPI ,booking_success_page ,CancelBookingAPI,VerifyPaymentAPI

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

    path(
        "invoice/<str:booking_id>/",
        views.view_invoice,
        name="view_invoice"
    ),
    path(
        "cancel-booking/<str:booking_id>/",
        CancelBookingAPI.as_view(),
    ),
    
    path(
        "cancel-reasons/",
        CancelReasonListAPI.as_view(),
    ),
    path(
        "cancel_booking_page/<str:booking_id>/",
        views.cancel_booking_page  ,name="cancel_booking_page"
    ),
    
    path("verify-payment/", VerifyPaymentAPI.as_view(), name="verify_payment"),


]


