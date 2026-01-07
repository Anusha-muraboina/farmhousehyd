# from django.shortcuts import render





from django.http import HttpResponse

def coupon(request):
    return HttpResponse("Hello, this is Blog Page")


# # Create your views here.
# from decimal import Decimal
# from django.http import JsonResponse
# from django.utils import timezone
# from django.views.decorators.http import require_POST
# from django.contrib.auth.decorators import login_required

# from .models import Coupon, CouponUsage
# from booking.models import Booking


# @require_POST
# @login_required
# def apply_coupon(request):
#     """
#     Apply coupon to a booking
#     """
#     coupon_code = request.POST.get("coupon")
#     booking_id = request.POST.get("booking_id")

#     if not coupon_code or not booking_id:
#         return JsonResponse({
#             "success": False,
#             "message": "Invalid request"
#         })

#     try:
#         booking = Booking.objects.get(id=booking_id, user=request.user)
#     except Booking.DoesNotExist:
#         return JsonResponse({
#             "success": False,
#             "message": "Booking not found"
#         })

#     try:
#         coupon = Coupon.objects.get(coupon__iexact=coupon_code)
#     except Coupon.DoesNotExist:
#         return JsonResponse({
#             "success": False,
#             "message": "Invalid coupon code"
#         })

#     today = timezone.now().date()

#     # ✅ Date validation
#     if coupon.coupon_start_date > today or coupon.coupon_end_date < today:
#         return JsonResponse({
#             "success": False,
#             "message": "Coupon expired or not active"
#         })

#     # ✅ Minimum spend
#     if coupon.minimum_spend and booking.sub_total < coupon.minimum_spend:
#         return JsonResponse({
#             "success": False,
#             "message": f"Minimum spend ₹{coupon.minimum_spend} required"
#         })

#     # ✅ Maximum spend
#     if coupon.maximum_spend and booking.sub_total > coupon.maximum_spend:
#         return JsonResponse({
#             "success": False,
#             "message": f"Coupon valid only up to ₹{coupon.maximum_spend}"
#         })

#     # ✅ Usage limit per user
#     if coupon.usage_limit_per_user:
#         used_count = CouponUsage.objects.filter(
#             coupon=coupon,
#             user=request.user
#         ).count()

#         if used_count >= coupon.usage_limit_per_user:
#             return JsonResponse({
#                 "success": False,
#                 "message": "Coupon usage limit exceeded"
#             })

#     # =========================
#     # CALCULATE DISCOUNT
#     # =========================
#     if coupon.discount_type == "fixed_amount":
#         discount = coupon.coupon_amount
#     else:
#         discount = (booking.sub_total * coupon.coupon_amount) / Decimal(100)

#     # Prevent over-discount
#     discount = min(discount, booking.sub_total)

#     # =========================
#     # SAVE BOOKING
#     # =========================
#     booking.coupon_applied = coupon
#     booking.discount_amount = discount
#     booking.total_amount = booking.sub_total - discount + booking.tax_price
#     booking.save()

#     # Track usage
#     CouponUsage.objects.create(
#         coupon=coupon,
#         user=request.user
#     )

#     return JsonResponse({
#         "success": True,
#         "message": "Coupon applied successfully",
#         "discount": float(discount),
#         "total": float(booking.total_amount)
#     })
