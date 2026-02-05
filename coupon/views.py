# from django.shortcuts import render





from django.http import HttpResponse

def coupon(request):
    return HttpResponse("Hello, this is Blog Page")


# # Create your views here.
from decimal import Decimal
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Coupon, CouponUsage
from booking.models import Booking
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from farmhouse.models import Farmhouse
from django.db.models import Q
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from coupon.models import Coupon
from farmhouse.models import Farmhouse


from django.db.models import Q
from decimal import Decimal
from django.utils import timezone

@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def validate_coupon(request):

    code = request.GET.get("code")
    farmhouse_id = request.GET.get("farmhouse")
    amount = Decimal(request.GET.get("amount", "0"))

    if not code:
        return Response({
            "valid": False,
            "message": "Coupon code required"
        })

    farmhouse = Farmhouse.objects.filter(
        id=farmhouse_id
    ).first()

    coupon = Coupon.objects.filter(
        code__iexact=code,
        is_active=True
    ).filter(
        Q(farmhouse=farmhouse) |
        Q(farmhouse__isnull=True)
    ).first()

    if not coupon:
        return Response({
            "valid": False,
            "message": "Invalid coupon for this farmhouse"
        })

    today = timezone.now().date()

    if not (coupon.start_date <= today <= coupon.end_date):
        return Response({
            "valid": False,
            "message": "Coupon expired"
        })

    if amount < coupon.min_booking_amount:
        return Response({
            "valid": False,
            "message": f"Minimum booking must be ₹{coupon.min_booking_amount}"
        })

    # ✅ REAL DISCOUNT
    discount = coupon.calculate_discount(amount)

    return Response({
        "valid": True,
        "id": coupon.id,
        "discount": float(discount),
        "message": f"Coupon applied! You saved ₹{discount}"
    })











@require_POST
@login_required
def apply_coupon(request):
    """
    Apply coupon to a booking
    """
    coupon_code = request.POST.get("coupon")
    booking_id = request.POST.get("booking_id")

    if not coupon_code or not booking_id:
        return JsonResponse({
            "success": False,
            "message": "Invalid request"
        })

    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Booking not found"
        })

    try:
        coupon = Coupon.objects.get(coupon__iexact=coupon_code)
    except Coupon.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Invalid coupon code"
        })

    today = timezone.now().date()

    # ✅ Date validation
    if coupon.coupon_start_date > today or coupon.coupon_end_date < today:
        return JsonResponse({
            "success": False,
            "message": "Coupon expired or not active"
        })

    # ✅ Minimum spend
    if coupon.minimum_spend and booking.sub_total < coupon.minimum_spend:
        return JsonResponse({
            "success": False,
            "message": f"Minimum spend ₹{coupon.minimum_spend} required"
        })

    # ✅ Maximum spend
    if coupon.maximum_spend and booking.sub_total > coupon.maximum_spend:
        return JsonResponse({
            "success": False,
            "message": f"Coupon valid only up to ₹{coupon.maximum_spend}"
        })

    # ✅ Usage limit per user
    if coupon.usage_limit_per_user:
        used_count = CouponUsage.objects.filter(
            coupon=coupon,
            user=request.user
        ).count()

        if used_count >= coupon.usage_limit_per_user:
            return JsonResponse({
                "success": False,
                "message": "Coupon usage limit exceeded"
            })

    # =========================
    # CALCULATE DISCOUNT
    # =========================
    if coupon.discount_type == "fixed_amount":
        discount = coupon.coupon_amount
    else:
        discount = (booking.sub_total * coupon.coupon_amount) / Decimal(100)

    # Prevent over-discount
    discount = min(discount, booking.sub_total)

    # =========================
    # SAVE BOOKING
    # =========================
    booking.coupon_applied = coupon
    booking.discount_amount = discount
    booking.total_amount = booking.sub_total - discount + booking.tax_price
    booking.save()

    # Track usage
    CouponUsage.objects.create(
        coupon=coupon,
        user=request.user
    )

    return JsonResponse({
        "success": True,
        "message": "Coupon applied successfully",
        "discount": float(discount),
        "total": float(booking.total_amount)
    })
