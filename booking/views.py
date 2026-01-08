from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


from decimal import Decimal
from datetime import timedelta, date

from decimal import Decimal
from datetime import timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.conf import settings
from django.utils import timezone

from farmhouse.models import Farmhouse
from .models import Booking, BlockedDate
from coupon.models import Coupon


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_booking_emails(booking):
    from django.conf import settings

    # ================= USER EMAIL =================
    user_html = render_to_string(
        "emails/user_booking_email.html",
        {"booking": booking}
    )

    user_email = EmailMultiAlternatives(
        subject="Booking Confirmed – Farmhouse",
        body="Your booking is confirmed",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.guest_email],
    )
    user_email.attach_alternative(user_html, "text/html")
    user_email.send(fail_silently=True)

    # ================= ADMIN EMAIL =================
    admin_email_address = getattr(
        settings,
        "ADMIN_EMAIL",
        settings.DEFAULT_FROM_EMAIL  # fallback
    )

    admin_html = render_to_string(
        "emails/admin_booking_email.html",
        {"booking": booking}
    )

    admin_email = EmailMultiAlternatives(
        subject=f"New Booking – {booking.booking_id}",
        body="New booking received",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[admin_email_address],
    )
    admin_email.attach_alternative(admin_html, "text/html")
    admin_email.send(fail_silently=True)


import razorpay
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def daterange(start, end):
    for n in range((end - start).days):
        yield start + timedelta(days=n)


def calculate_price(farmhouse, check_in, check_out, extra_guests):
    total = Decimal("0.00")
    for d in daterange(check_in, check_out):
        total += farmhouse.get_price_by_date(d)
    total += Decimal(extra_guests) * farmhouse.pricing.extra_guest_price
    return total


def farmhouse_detail(request, slug):
    farmhouse = get_object_or_404(Farmhouse, slug=slug, is_active=True)

    # BOOKED DATES
    booked_dates = []
    for b in farmhouse.bookings.filter(status__in=["pending", "confirmed"]):
        for d in daterange(b.check_in, b.check_out):
            booked_dates.append(d.strftime("%Y-%m-%d"))

    # BLOCKED DATES (FIXED)
    blocked_dates = []
    for block in BlockedDate.objects.all():
        cur = block.start_date
        while cur <= block.end_date:
            blocked_dates.append(cur.strftime("%Y-%m-%d"))
            cur += timedelta(days=1)

    if request.method == "POST":
        with transaction.atomic():

            check_in = date.fromisoformat(request.POST["check_in"])
            check_out = date.fromisoformat(request.POST["check_out"])

            sub_total = calculate_price(
                farmhouse,
                check_in,
                check_out,
                int(request.POST.get("extra_guest_count", 0))
            )

            discount = Decimal("0.00")
            coupon = None
            code = request.POST.get("coupon_code")

            if code:
                try:
                    coupon = Coupon.objects.get(code__iexact=code)
                    if coupon.is_valid():
                        discount = coupon.calculate_discount(sub_total)
                except Coupon.DoesNotExist:
                    pass

            total = sub_total - discount

            booking = Booking.objects.create(
                farmhouse=farmhouse,
                guest_name=request.POST["guest_name"],
                guest_email=request.POST["guest_email"],
                guest_phone=request.POST["guest_phone"],
                guest_count=request.POST["guest_count"],
                extra_guest_count=request.POST.get("extra_guest_count", 0),
                check_in=check_in,
                check_out=check_out,
                check_in_time=request.POST.get("check_in_time"),
                check_out_time=request.POST.get("check_out_time"),
                special_requests=request.POST.get("special_requests", ""),
                sub_total=sub_total,
                disc_price=discount,
                total_amount=total,
                coupon_applied=coupon,
                payment_method=request.POST["payment_method"],
            )

            # PAY AT FARMHOUSE
            if booking.payment_method == "farmhouse":
                booking.status = "confirmed"
                booking.save()
                send_booking_emails(booking)
                return redirect("booking_confirmation", booking.booking_id)

            # RAZORPAY
            order = razorpay_client.order.create({
                "amount": int(total * 100),
                "currency": "INR",
                "payment_capture": 1
            })

            booking.transaction_id = order["id"]
            booking.save()

            return render(request, "razorpay_checkout.html", {
                "order": order,
                "razorpay_key": settings.RAZORPAY_KEY_ID
            })

    return render(request, "farmhouse_detail.html", {
        "farmhouse": farmhouse,
        "booked_dates": booked_dates,
        "blocked_dates": blocked_dates,
    })



def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, "booking_confirmation.html", {"booking": booking})

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


@csrf_exempt
def verify_razorpay_payment(request):
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

    send_booking_emails(booking)

    return redirect("booking_confirmation", booking.booking_id)

