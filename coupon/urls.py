from django.urls import path
from .views import *

urlpatterns = [
    path("apply-coupon/", apply_coupon, name="apply_coupon"),
    path("validate-coupon/", validate_coupon ,name="validate-coupon"),
]
