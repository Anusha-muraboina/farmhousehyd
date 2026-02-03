from django.urls import path
from . import views

from .views import create_farmhouse_booking, razorpay_webhook

urlpatterns = [
        path("api/create-booking/", create_farmhouse_booking),
        path("razorpay-webhook/", razorpay_webhook),

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
