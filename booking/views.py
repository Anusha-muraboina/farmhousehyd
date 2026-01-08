from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


from decimal import Decimal
from datetime import timedelta, date

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from farmhouse.models import Farmhouse
from .models import Booking, BlockedDate
from coupon.models import Coupon

# Razorpay
import razorpay
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

# =========================
# HELPER: DATE RANGE
# =========================
def daterange(start, end):
    for n in range((end - start).days):
        yield start + timedelta(days=n)

# =========================
# HELPER: PRICE CALCULATION
# =========================
def calculate_price(farmhouse, check_in, check_out, guests, extra_guests):
    nights = (check_out - check_in).days
    base_price = Decimal("0.00")

    for single_date in daterange(check_in, check_out):
        base_price += farmhouse.get_price_by_date(single_date)

    extra_price = Decimal(extra_guests) * farmhouse.pricing.extra_guest_price
    return base_price + extra_price

# =========================
# FARMHOUSE DETAIL + BOOKING
# =========================
def farmhouse_detail(request, slug):
    farmhouse = get_object_or_404(Farmhouse, slug=slug, is_active=True)

    # ---- BOOKED DATES (CONFIRMED + PENDING) ----
    booked_dates = []
    bookings = farmhouse.bookings.filter(
        status__in=["pending", "confirmed"],
        check_out__gte=timezone.now().date()
    )

    for booking in bookings:
        for d in daterange(booking.check_in, booking.check_out):
            booked_dates.append(d.strftime("%Y-%m-%d"))

    # ---- BLOCKED DATES ----
    blocked_dates = []
    blocks = farmhouse.blocked_dates.all()

    for block in blocks:
        current = block.start_date
        while current <= block.end_date:
            blocked_dates.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

    # ---- BOOKING SUBMIT ----
    if request.method == "POST":
        with transaction.atomic():

            check_in = date.fromisoformat(request.POST["check_in"])
            check_out = date.fromisoformat(request.POST["check_out"])

            guest_count = int(request.POST["guest_count"])
            extra_guest_count = int(request.POST.get("extra_guest_count", 0))

            payment_method = request.POST["payment_method"]
            coupon_code = request.POST.get("coupon_code", "").strip()

            sub_total = calculate_price(
                farmhouse,
                check_in,
                check_out,
                guest_count,
                extra_guest_count
            )

            discount = Decimal("0.00")
            coupon = None

            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code__iexact=coupon_code)
                    if coupon.is_valid():
                        discount = coupon.calculate_discount(sub_total)
                except Coupon.DoesNotExist:
                    pass

            tax = Decimal("0.00")
            total = sub_total - discount + tax

            booking = Booking.objects.create(
                farmhouse=farmhouse,
                guest_name=request.POST["guest_name"],
                guest_email=request.POST["guest_email"],
                guest_phone=request.POST["guest_phone"],
                guest_count=guest_count,
                extra_guest_count=extra_guest_count,
                check_in=check_in,
                check_out=check_out,
                check_in_time=request.POST["check_in_time"],
                check_out_time=request.POST["check_out_time"],
                special_requests=request.POST.get("special_requests", ""),
                sub_total=sub_total,
                discount_amount=discount,
                tax_price=tax,
                total_amount=total,
                coupon_applied=coupon,
                payment_method=payment_method,
                status="pending",
                payment_status="pending",
            )

            # ---- PAY AT FARMHOUSE ----
            if payment_method == "farmhouse":
                booking.status = "confirmed"
                booking.save()
                return redirect("booking_confirmation", booking.booking_id)

            # ---- RAZORPAY ----
            order_amount = int(total * 100)

            order = razorpay_client.order.create({
                "amount": order_amount,
                "currency": "INR",
                "payment_capture": 1
            })

            booking.transaction_id = order["id"]
            booking.save()

            return render(request, "bookings/razorpay_checkout.html", {
                "booking": booking,
                "order": order,
                "razorpay_key": settings.RAZORPAY_KEY_ID
            })

    return render(request, "farmhouse/farmhouse_detail.html", {
        "farmhouse": farmhouse,
        "booked_dates": booked_dates,
        "blocked_dates": blocked_dates,
    })

# =========================
# COUPON VALIDATION (AJAX)
# =========================
def validate_coupon(request):
    code = request.GET.get("code", "")
    amount = Decimal(request.GET.get("amount", "0"))

    try:
        coupon = Coupon.objects.get(code__iexact=code)
        if coupon.is_valid():
            discount = coupon.calculate_discount(amount)
            return JsonResponse({"valid": True, "discount": float(discount)})
    except Coupon.DoesNotExist:
        pass

    return JsonResponse({"valid": False, "discount": 0})

# =========================
# RAZORPAY VERIFY
# =========================
@csrf_exempt
def verify_razorpay_payment(request):
    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": request.POST["razorpay_order_id"],
            "razorpay_payment_id": request.POST["razorpay_payment_id"],
            "razorpay_signature": request.POST["razorpay_signature"],
        })

        booking = Booking.objects.get(
            transaction_id=request.POST["razorpay_order_id"]
        )

        booking.payment_status = "paid"
        booking.status = "confirmed"
        booking.payment_id = request.POST["razorpay_payment_id"]
        booking.save()

        return redirect("booking_confirmation", booking.booking_id)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# =========================
# BOOKING CONFIRMATION
# =========================
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, "bookings/booking_confirmation.html", {
        "booking": booking
    })
