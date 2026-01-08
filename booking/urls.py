from django.urls import path
from . import views

urlpatterns = [

    # =======================
    # BOOKING FLOW
    # =======================

    # Farmhouse / Room detail + booking page
    path(
        "farmhouse/<slug:slug>/",
        views.room_detail,
        name="room_detail"
    ),

    # Booking confirmation page
    path(
        "booking/confirmation/<str:booking_id>/",
        views.booking_confirmation,
        name="booking_confirmation"
    ),

    # =======================
    # PAYMENT (RAZORPAY)
    # =======================

    # Create Razorpay order
    path(
        "payment/create-order/",
        views.create_razorpay_order,
        name="create_razorpay_order"
    ),

    # Verify Razorpay payment (after checkout)
    path(
        "payment/verify/",
        views.verify_razorpay_payment,
        name="verify_razorpay_payment"
    ),

    # Razorpay webhook
    path(
        "payment/webhook/",
        views.razorpay_webhook,
        name="razorpay_webhook"
    ),

    # Payment processing waiting page
    path(
        "payment/processing/",
        views.payment_processing,
        name="payment_processing"
    ),

    # Poll booking status
    path(
        "payment/check-status/",
        views.check_booking_status,
        name="check_booking_status"
    ),

    # =======================
    # COUPON
    # =======================

    # Validate coupon via AJAX
    path(
        "coupon/validate/",
        views.validate_coupon,
        name="validate_coupon"
    ),

    # =======================
    # INVOICE
    # =======================

    # View invoice
    path(
        "invoice/<str:booking_id>/",
        views.view_invoice,
        name="view_invoice"
    ),

]

