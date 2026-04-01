from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal
from datetime import datetime
import razorpay
from django.conf import settings
from django.shortcuts import render
from .models import Booking
from farmhouse.models import Farmhouse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.contrib.auth import login
from datetime import timedelta
from farmhouse.models import FarmhousePricing
from rest_framework.permissions import IsAuthenticated
from wallet.models import Wallet, WalletHistory
from django.urls import reverse
from django.http import JsonResponse
# from .utils import calculate_booking_cost
from booking.models import *
from booking.serializers import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


from rest_framework.authentication import SessionAuthentication


import json
import razorpay
from decimal import Decimal

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import BookingSerializer
from .models import Booking

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BlockedDate

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from wallet.views import apply_wallet_to_booking

import razorpay
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .models import Booking






client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

# @api_view(["GET"])
# @authentication_classes([])
# @permission_classes([AllowAny])
# def blocked_dates_api(request, farmhouse_id):

#     blocked_ranges = []

#     ###################################
#     # ✅ ADMIN BLOCKED DATES
#     ###################################

#     admin_blocks = BlockedDate.objects.filter(
#         farmhouse_id=farmhouse_id
#     )

#     for b in admin_blocks:
#         blocked_ranges.append({
#             "from": b.start_date,
#             "to": b.end_date - timedelta(days=1)  # allow checkout
#         })

#     ###################################
#     # ✅ CONFIRMED BOOKINGS
#     ###################################

#     bookings = Booking.objects.filter(
#         farmhouse_id=farmhouse_id,
#         status="confirmed"
#     )

#     for booking in bookings:
#         blocked_ranges.append({
#             "from": booking.check_in,
#             "to": booking.check_out - timedelta(days=1)  # allow checkout
#         })

#     return Response(blocked_ranges)




    # return Response(blocked_ranges)


User = get_user_model()
class CreateBookingAPI(APIView):

    authentication_classes = []   #  REMOVE BASIC AUTH (causing 401)
    permission_classes = [AllowAny]

    def post(self, request):

        data = request.data.copy()

        farmhouse_id = data.get("farmhouse")
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        extra_guest_count = int(data.get("extra_guest_count", 0))
        # coupon_code = data.get("coupon_code")
        coupon_id = data.get("coupon_applied")

        ###################################
        # GET FARMHOUSE PRICING
        ###################################

        try:
            farmhouse = Farmhouse.objects.select_related("pricing").get(id=farmhouse_id)
        except Farmhouse.DoesNotExist:
            return Response({"error": "Invalid farmhouse"}, status=400)

        # pricing = farmhouse.pricing
        pricing = getattr(farmhouse, "pricing", None)

        if not pricing:
            return Response(
                {"error": "Pricing not configured for this farmhouse"},
                status=400
            )

        normal_price = pricing.normal_day_price
        weekend_price = pricing.weekend_price
        extra_price = pricing.extra_guest_price
        sale_price = pricing.sale_price

# 
        ###################################
        # SERVER SIDE PRICE CALCULATION
        ###################################

        start = datetime.strptime(check_in, "%Y-%m-%d")
        end = datetime.strptime(check_out, "%Y-%m-%d")
        ###################################
        # 🚨 PREVENT DOUBLE BOOKING
        ###################################

        overlap = Booking.objects.filter(
            farmhouse_id=farmhouse_id,
            status="confirmed",
            # status__in=[ "confirmed"],  # important
            # status="confirmed",
            check_in__lt=end,
            check_out__gt=start
        ).exists()

        if overlap:
            return Response(
                {"error": "Selected dates are already booked"},
                status=400
            )

        ###################################
        # ❌ CHECK BLOCKED DATES ALSO
        ###################################
        blocked_conflict = BlockedDate.objects.filter(
            farmhouse_id=farmhouse_id,
            start_date__lt=end,
            end_date__gt=start
        ).exists()

        if blocked_conflict:
            return Response(
                {"error": "These dates are blocked"},
                status=400
            )



        sub_total = Decimal("0.00")

        while start < end:
            if sale_price and sale_price > 0:

                sub_total += sale_price

            else:

                # Saturday=5, Sunday=6
                if start.weekday() in [5, 6]:
                    sub_total += weekend_price
                else:
                    sub_total += normal_price

            start += timedelta(days=1)
            # Saturday=5, Sunday=6
            # if start.weekday() in [5, 6]:
            #     sub_total += weekend_price
            # else:
            #     sub_total += normal_price

            # start += timedelta(days=1)

        sub_total += extra_guest_count * extra_price


        ############################################
        # CREATE / ATTACH USER
        ############################################

        is_new_user = False
        password = None

        if request.user.is_authenticated:

            user = request.user

        else:

            email = data.get("guest_email")
            name = data.get("guest_name")

            user = User.objects.filter(email=email).first()

            if not user:

                password = get_random_string(10)

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=name,
                    password=password
                )

                is_new_user = True

                # ⭐ AUTO LOGIN
                login(request, user)

                is_new_user = True
        ###################################
        # APPLY COUPON (SAFE)
        ###################################

        discount = Decimal("0.00")
        coupon_obj = None

        # if coupon_code:

        #     coupon = Coupon.objects.filter(
        #         code__iexact=coupon_code,
        #         is_active=True
        #     ).first()

        #     if coupon and coupon.is_valid():

        #         if sub_total >= coupon.min_booking_amount:
        #             discount = coupon.calculate_discount(sub_total)
        #             coupon_obj = coupon
        if coupon_id:

            coupon_obj = Coupon.objects.filter(
                id=coupon_id,
                is_active=True
            ).filter(
                Q(farmhouse=farmhouse) |
                Q(farmhouse__isnull=True)
            ).first()

            if not coupon_obj:
                return Response(
                    {"error":"Invalid coupon"},
                    status=400
                )

            if not coupon_obj.is_valid():
                return Response(
                    {"error":"Coupon expired"},
                    status=400
                )

            if sub_total < coupon_obj.min_booking_amount:
                return Response(
                    {"error":f"Minimum booking must be ₹{coupon_obj.min_booking_amount}"},
                    status=400
                )

            discount = coupon_obj.calculate_discount(sub_total)

        ###################################
        total_amount = max(sub_total - discount, Decimal("0.00"))
        

        # ###################################
        # # APPLY WALLET AFTER BOOKING SAVE
        # ###################################

        # wallet_used = Decimal("0.00")
        # use_wallet = str(data.get("use_wallet")).lower() in ["true", "1"]

        # if use_wallet:

        #     wallet = Wallet.objects.filter(user=user).first()

        #     if wallet and wallet.balance > 0:

        #         wallet_used = min(wallet.balance, booking.total_amount)

        #         wallet.balance -= wallet_used
        #         wallet.save()

        #         booking.wallet_used = wallet_used
        #         booking.total_amount -= wallet_used
        #         booking.remaining_amount = booking.total_amount

        #         booking.save()

        #         WalletHistory.objects.create(
        #             user=user,
        #             amount=wallet_used,
        #             transaction_type="debit",
        #             description=f"Wallet used for booking {booking.booking_id}"
        #         )
        ###################################
        # ALWAYS UPDATE DATA
        ###################################

        data["sub_total"] = sub_total
        data["disc_price"] = discount
        data["total_amount"] = total_amount
        # data["wallet_used"] = wallet_used
        data["coupon_applied"] = coupon_obj.id if coupon_obj else None
        ###################################
        # SAVE BOOKING
        ###################################

        serializer = BookingSerializer(data=data , 
                                   context={"request": request}    
                                       
                                       )

        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=400)


        serializer.is_valid(raise_exception=True)
        
        
        booking = serializer.save(
            user=user,
            sub_total=sub_total,
            disc_price=discount,
            total_amount=total_amount,
            remaining_amount=total_amount,
            payment_status="pending",
            status="pending", 
            coupon_applied=coupon_obj,
        )
        
        # sync_to_vivaan(booking)
        sync_booking_to_vivaan(booking)
        # ✅ FIXED WALLET FLAG
        use_wallet = str(request.data.get("use_wallet")).lower() in ["true", "1"]

        # ✅ APPLY WALLET
        if use_wallet:
            apply_wallet_to_booking(booking)
            booking.refresh_from_db()
        # use_wallet = data.get("use_wallet") in [True, "true", "1", 1]

        # if use_wallet:
        #     apply_wallet_to_booking(booking)
        #     booking.refresh_from_db()
       ###################################
        # APPLY WALLET
        ###################################

      
        # Apply wallet
        # apply_wallet_to_booking(booking)
        ###################################
        # AUTO CREATE INVOICE ⭐⭐⭐⭐⭐
        ###################################

        # Invoice.objects.create(
        #     booking=booking,
        #     user=user,
        #     invoice_id=f"INV-{get_random_string(8)}"
        # )
        ############################################
        # SEND ACCOUNT EMAIL IF NEW USER
        ############################################

        if is_new_user:

            send_mail(
                subject="Your Farmhouse Hyd Account Created 🎉",
                message=f"""
        Welcome to Farmhouse Hyd!

        Your account was created automatically during booking.

        LOGIN DETAILS:

        Email: {user.email}
        Password: {password}

        Login:
        https://yourdomain.com/login

        IMPORTANT:
        Please change your password after login.
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )


        # booking = serializer.save(
        #         sub_total=sub_total,
        #         disc_price=discount,
        #         total_amount=total_amount,
        #         coupon_applied=coupon_obj
            
            
        # )

        # booking = serializer.save()
        # booking = serializer.save(
        #     status="pending",
        #     payment_status="pending"
        # )
        ################################
        # PAY AT FARMHOUSE
        ################################
        if booking.payment_method == "farmhouse":

            booking.status = "pending"
            booking.payment_status = "pending"
            booking.save()

            return Response({
                "redirect_url": f"/bookings/booking-success/{booking.id}/"
            })

        # if booking.payment_method == "farmhouse":

        #     booking.status = "confirmed"
        #     booking.save()

        #     return Response({
        #         "redirect_url": f"/bookings/booking-success/{booking.id}/"
        #     })

        ################################
        # RAZORPAY
        ################################
        payable_amount = booking.total_amount

        if booking.payment_method == "partial_razorpay":
            # amount = int(booking.total_amount * Decimal("0.30") * 100)
            # amount = int((booking.total_amount * Decimal("0.30")).quantize(Decimal("1")))
            # amount *= 100
            payable_amount = (payable_amount * Decimal("0.30")).quantize(Decimal("0.01"))
            amount = int(payable_amount * 100)
        
        else:
            # amount = int(booking.total_amount * 100)
            amount = int(booking.total_amount.quantize(Decimal("1"))) * 100

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        booking.transaction_id = order["id"]
        booking.save()

        return Response({
            "user": user,
            "key": settings.RAZORPAY_KEY_ID,
            "amount": amount,
            "order_id": order["id"],
            "booking_id": booking.id,
            "wallet_used": booking.wallet_used
        })













@csrf_exempt
def razorpay_webhook(request):

    webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET

    body = request.body
    signature = request.headers.get('X-Razorpay-Signature')

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    # ✅ VERIFY SIGNATURE
    try:
        client.utility.verify_webhook_signature(
            body,
            signature,
            webhook_secret
        )
    except razorpay.errors.SignatureVerificationError:
        return HttpResponse(status=400)

    payload = json.loads(body)
    event = payload.get("event")

    ###################################
    # PAYMENT CAPTURED
    ###################################

    # if event == "payment.captured":
    if event in ["payment.captured", "payment.authorized"]:
        

        payment = payload["payload"]["payment"]["entity"]
        order_id = payment["order_id"]

        booking = Booking.objects.filter(
            transaction_id=order_id
        ).first()

        if not booking:
            return HttpResponse(status=200)

        # ✅ prevent double processing
        if booking.payment_status in ["paid", "partial"]:
            return HttpResponse(status=200)

    ###################################

        if booking.payment_method == "full_razorpay":

            booking.payment_status = "paid"
            booking.remaining_amount = Decimal("0.00")
            booking.status = "confirmed"

        ###################################
        # PARTIAL PAYMENT
        ###################################

        elif booking.payment_method == "partial_razorpay":

            paid_amount = booking.total_amount * Decimal("0.30")

            booking.payment_status = "partial"
            booking.remaining_amount = booking.total_amount - paid_amount
            booking.status = "confirmed"

        ###################################

        booking.payment_id = payment["id"]
        booking.save()
        sync_booking_to_vivaan(booking)
        # if booking.payment_method == "partial_razorpay":
        #     booking.payment_status = "partial"
        #     booking.remaining_amount = booking.total_amount * Decimal("0.70")

        # else:
        #     booking.payment_status = "paid"
        #     booking.remaining_amount = Decimal("0.00")

        # booking.status = "confirmed"
        # booking.payment_id = payment["id"]

        # booking.save()

    return HttpResponse("OK")

# 


from django.shortcuts import get_object_or_404
class BookingSuccessAPI(APIView):

    authentication_classes = []   # 🔥 REMOVE BASIC AUTH (causing 401)
    permission_classes = [AllowAny]
    def get(self, request, booking_id):

        booking = get_object_or_404(
            Booking.objects.select_related("farmhouse"),
            id=booking_id
        )
        
        
                ############################################
        # ⭐ CREATE INVOICE IF NOT EXISTS
        ############################################
        Invoice.objects.get_or_create(
            booking=booking,
            defaults={"user": booking.user}
        )

        return Response({

            "booking_id": booking.booking_id,
            "farmhouse": booking.farmhouse.title,

            "guest_name": booking.guest_name,
            "guest_phone": booking.guest_phone,
            "guest_email": booking.guest_email,

            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "wallet_used": booking.wallet_used, 
            "guest_count": booking.guest_count,
            "extra_guest_count": booking.extra_guest_count,

            "sub_total": booking.sub_total,
            "discount": booking.disc_price,
            "total_amount": booking.total_amount,
            "advance_paid": booking.advance_paid,
            "remaining_amount": booking.remaining_amount,

            "payment_status": booking.payment_status,
            "payment_method": booking.payment_method,
            "status": booking.status,
        })



def booking_success_page(request, booking_id):

    return render(
        request,
        "booking_confirmation.html",
        {"booking_id": booking_id}
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from booking.models import Invoice


# @login_required
# def view_invoice(request, booking_id):
#     invoice = get_object_or_404(
#         Invoice.objects.select_related(
#             "booking",
#             "booking__farmhouse"
#         ),
#         booking__booking_id=booking_id,
#         booking__user=request.user
#     )

#     return render(
#         request,
#         "emails/invoice.html",
#         {
#             "invoice": invoice,
#             "booking": invoice.booking
#         }
#     )

def view_invoice(request, booking_id):

    booking = get_object_or_404(
        Booking.objects.select_related("farmhouse"),
        booking_id=booking_id
    )

    invoice, _ = Invoice.objects.get_or_create(
        booking=booking,
        defaults={"user": booking.user}
    )

    return render(
        request,
        "emails/invoice.html",
        {
            "invoice": invoice,
            "booking": booking
        }
    )



class CancelReasonListAPI(ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = CancelReason.objects.filter(is_active=True)
    serializer_class = CancelReasonSerializer
    
    
    


class CancelBookingAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):

        try:
            booking = Booking.objects.get(
                booking_id=booking_id,
                user=request.user
            )

        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=404
            )

        reason_id = request.data.get("reason")
        comment = request.data.get("comment", "")

        reason = None

        if reason_id:
            reason = CancelReason.objects.filter(
                id=reason_id
            ).first()

        try:

            booking.cancel_booking(
                user=request.user,
                reason=reason,
                comment=comment
            )

        except ValidationError as e:

            return Response(
                {"error": str(e)},
                status=400
            )

        return Response({
            "message": "Booking cancelled successfully"
        })
        
        
@login_required
def cancel_booking_page(request, booking_id):

    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,   # using booking code 👍
        user=request.user
    )

    return render(
        request,
        "cancelled_booking.html",
        {
            "booking": booking   # ⭐ PASS OBJECT, not just id
        }
    )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from decimal import Decimal
from .models import Booking


class VerifyPaymentAPI(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        order_id = request.data.get("order_id")
        payment_id = request.data.get("payment_id")

        booking = Booking.objects.filter(
            transaction_id=order_id
        ).first()

        if not booking:
            return Response({"error": "Booking not found"}, status=404)

        # Prevent duplicate update
        if booking.payment_status in ["paid", "partial"]:
            return Response({"message": "Already updated"})

        ###################################
        # FULL PAYMENT
        ###################################
        if booking.payment_method == "full_razorpay":

            booking.payment_status = "paid"
            booking.remaining_amount = Decimal("0.00")

        ###################################
        # PARTIAL PAYMENT
        ###################################
        else:

            paid_amount = (
                booking.total_amount * Decimal("0.30")
            ).quantize(Decimal("0.01"))

            booking.payment_status = "partial"
            booking.remaining_amount = booking.total_amount - paid_amount

        booking.status = "confirmed"
        booking.payment_id = payment_id
        booking.save()
        sync_booking_to_vivaan(booking)

        return Response({"message": "Payment verified"})







# def sync_to_vivaan(booking):

#     # ✅ ONLY FOR VIVAAN
#     if booking.farmhouse.slug != "vivaan-farmhouse":
#         return

#     import requests

#     try:
#         requests.post(
#             "https://vivaanfarmhouse.com/api/vivaan/receive-booking/",
#             json={
#                 "check_in": str(booking.check_in),
#                 "check_out": str(booking.check_out),
#             },
#             timeout=3
#         )
#     except Exception as e:
#         print("Vivaan sync error:", e)
        
        
        

# @api_view(["POST"])
# def vivaan_receive_booking(request):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     data = request.data

#     slug = data.get("farmhouse_slug")

#     farmhouse = Farmhouse.objects.get(slug=slug)  # ✅ dynamic

#     check_in = datetime.strptime(data["check_in"], "%Y-%m-%d").date()
#     check_out = datetime.strptime(data["check_out"], "%Y-%m-%d").date()

#     end_date = check_out - timedelta(days=1)

#     exists = BlockedDate.objects.filter(
#         farmhouse=farmhouse,
#         start_date=check_in,
#         end_date=end_date
#     ).exists()

#     if not exists:
#         BlockedDate.objects.create(
#             farmhouse=farmhouse,
#             start_date=check_in,
#             end_date=end_date,
#             reason="Vivaan booking"
#         )

#     return Response({"status": "ok"})

# @api_view(["GET"])
# def blocked_dates_api_vivaan(request, farmhouse_id):

#     disabled_dates = set()

#     ###################################
#     # ✅ LOCAL BOOKINGS
#     ###################################
#     bookings = Booking.objects.filter(
#         farmhouse_id=farmhouse_id,
#         status="confirmed"
#     )

#     for booking in bookings:
#         current = booking.check_in
#         while current < booking.check_out:
#             disabled_dates.add(current.strftime("%Y-%m-%d"))
#             current += timedelta(days=1)

#     ###################################
#     # ✅ LOCAL BLOCKED
#     ###################################
#     blocks = BlockedDate.objects.filter(
#         farmhouse_id=farmhouse_id
#     )

#     for block in blocks:
#         current = block.start_date
#         while current <= block.end_date:
#             disabled_dates.add(current.strftime("%Y-%m-%d"))
#             current += timedelta(days=1)

#     ###################################
#     # 🔥 VIVAAN SYNC (FIXED)
#     ###################################
#     import requests
#     from datetime import datetime
#     from farmhouse.models import Farmhouse

#     farmhouse = Farmhouse.objects.get(id=farmhouse_id)

#     if farmhouse.slug == "vivaan-farmhouse":

#         try:
#             res = requests.get(
#                 "https://vivaanfarmhouse.com/api/vivaan/blocked-dates/",
#                 timeout=3
#             )

#             if res.status_code == 200:
#                 data = res.json()

#                 for item in data:
#                     start = datetime.strptime(item["from"], "%Y-%m-%d").date()
#                     end = datetime.strptime(item["to"], "%Y-%m-%d").date()

#                     current = start

#                     while current <= end:
#                         disabled_dates.add(current.strftime("%Y-%m-%d"))
#                         current += timedelta(days=1)

#         except Exception as e:
#             print("Vivaan fetch error:", e)

#     ###################################
#     return Response({
#         "disabled_dates": sorted(list(disabled_dates))
#     })



# booking/views.py
import requests
from django.conf import settings
import requests
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BlockedDate


def sync_booking_to_vivaan(booking):
    """Sync confirmed booking from Hyd → Vivaan website"""
    # if not booking.room_category or booking.room_category.slug != "vivaan-farmhouse":
    #     return

    # ✅ ONLY CONFIRMED BOOKINGS (OR PENDING PAY AT FARMHOUSE)
    if booking.status != "confirmed" and not (booking.status == "pending" and booking.payment_method == "farmhouse"):
        return

    # ✅ FIXED FIELD (IMPORTANT)
    if not booking.farmhouse or booking.farmhouse.slug != "vivaan-farmhouse":
        return

    try:
        from django.conf import settings
        webhook_url = "http://127.0.0.1:8000/api/vivaan/receive-booking/" if getattr(settings, 'DEBUG', False) else "https://vivaanfarmhouse.com/api/vivaan/receive-booking/"
        requests.post(
            webhook_url,
            json={
                "check_in": str(booking.check_in),
                "check_out": str(booking.check_out),
                "booking_id": booking.booking_id,
                "source": "farmhouse_hyd"
            },
            timeout=8,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Synced to Vivaan: {booking.booking_id}")
    except Exception as e:
        print(f"❌ Sync to Vivaan failed: {e}")


@api_view(["POST"])
@permission_classes([AllowAny])
def receive_booking_from_vivaan(request):
    """Vivaan site sends booking here"""
    try:
        data = request.data
        check_in = datetime.strptime(data["check_in"], "%Y-%m-%d").date()
        check_out = datetime.strptime(data["check_out"], "%Y-%m-%d").date()
        # end_date = check_out - timedelta(days=1)
        # We store check_out as end_date (non-inclusive) to match ICAL/Booking patterns
        end_date = check_out

        if not BlockedDate.objects.filter(farmhouse_id=65, start_date=check_in, end_date=end_date).exists():
            BlockedDate.objects.create(
                farmhouse_id=65,  # Important: ID for Vivaan Farmhouse
                start_date=check_in,
                end_date=end_date,
                reason="Booking from Vivaan Farmhouse website"
            )
            print(f"✅ Blocked on Hyd: {check_in} to {end_date}")

        return Response({"status": "ok"})
    except Exception as e:
        print(f"Error: {e}")
        return Response({"error": str(e)}, status=500)
    


# @api_view(["GET"])
# @authentication_classes([])
# @permission_classes([AllowAny])
# def blocked_dates_api(request, farmhouse_id):
#     blocked_ranges = []

#     # Admin Blocked Dates
#     admin_blocks = BlockedDate.objects.filter(farmhouse_id=farmhouse_id)
#     for b in admin_blocks:
#         blocked_ranges.append({
#             "from": b.start_date,
#             "to": b.end_date - timedelta(days=1)
#         })

#     # Confirmed Bookings for this farmhouse
#     bookings = Booking.objects.filter(
#         # Q(status="confirmed") | Q(status="pending", payment_method="farmhouse"),
#         farmhouse_id=farmhouse_id ,
#         status="confirmed", 
#     )
#     for booking in bookings:
#         blocked_ranges.append({
#             "from": booking.check_in,
#             "to": booking.check_out - timedelta(days=1)
#         })

#     # Extra: If this is Vivaan Farmhouse, try to fetch latest from Vivaan site
#     try:
#         farmhouse = Farmhouse.objects.get(id=farmhouse_id)
#         if farmhouse.slug == "vivaan-farmhouse":
#             try:
#                 from django.conf import settings
#                 external_url = "https://vivaanfarmhouse.com/api/blocked-dates/" if getattr(settings, 'DEBUG', False) else "https://vivaanfarmhouse.com/api/blocked-dates/"
#                 res = requests.get(
#                     external_url,
#                     timeout=5
#                 )
#                 if res.status_code == 200:
#                     data = res.json()
#                     for item in data.get("disabled_dates", []):
#                         d = datetime.strptime(item, "%Y-%m-%d").date()
#                         blocked_ranges.append({"from": d, "to": d})
#             except:
#                 pass  # silent if Vivaan is down
#     except:
#         pass

#     return Response(blocked_ranges)









@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def blocked_dates_api(request, farmhouse_id):
    blocked_ranges = []

    # 1. ADMIN BLOCKED
    admin_blocks = BlockedDate.objects.filter(farmhouse_id=farmhouse_id)
    for b in admin_blocks:
        blocked_ranges.append({
            "from": b.start_date,
            "to": b.end_date - timedelta(days=1)
        })

    # 2. BOOKINGS
    bookings = Booking.objects.filter(
        farmhouse_id=farmhouse_id,
        status="confirmed",
    )
    for booking in bookings:
        blocked_ranges.append({
            "from": booking.check_in,
            "to": booking.check_out - timedelta(days=1)
        })

    # 3.  SYNC FROM VIVAAN (FIXED)
    try:
        farmhouse = Farmhouse.objects.get(id=farmhouse_id)

        if farmhouse.slug == "vivaan-farmhouse":
            try:
                external_url = "https://vivaanfarmhouse.com/api/blocked-dates/"

                res = requests.get(external_url, timeout=5)

                if res.status_code == 200:
                    data = res.json()

                    for item in data.get("disabled_dates", []):
                        d = datetime.strptime(item, "%Y-%m-%d").date()

                        blocked_ranges.append({
                            "from": d,
                            "to": d
                        })

            except Exception as e:
                print("Sync error:", e)

    except Exception as e:
        print("Farmhouse error:", e)

    return Response(blocked_ranges)