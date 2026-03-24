from django.shortcuts import render
from django.http import HttpResponse
from decimal import Decimal

from wallet.models import Wallet, WalletHistory
from booking.models import Booking


###########################################################
# SIMPLE TEST VIEW
###########################################################

def wallet(request):
    return HttpResponse("Hello, this is Wallet Page")


###########################################################
# ADMIN WALLET CREDIT FUNCTION
###########################################################

def add_wallet_credit(user, amount, description="Admin wallet credit"):
    """
    Adds money to a user's wallet.
    Example: Admin gives ₹2000 wallet credit
    """

    wallet, created = Wallet.objects.get_or_create(user=user)

    wallet.balance += Decimal(amount)
    wallet.save()

    WalletHistory.objects.create(
        user=user,
        amount=amount,
        transaction_type="credit",
        description=description
    )

    return wallet


###########################################################
# APPLY WALLET TO BOOKING
###########################################################




from django.db import transaction

@transaction.atomic
def apply_wallet_to_booking(booking):
    wallet = Wallet.objects.select_for_update().filter(user=booking.user).first()

    if not wallet or wallet.balance <= 0:
        return booking

    wallet_used = Decimal("0.00")

    if wallet.balance >= booking.total_amount:
        wallet_used = booking.total_amount
        wallet.balance -= wallet_used

        booking.total_amount = Decimal("0.00")
        booking.remaining_amount = Decimal("0.00")

    else:
        wallet_used = wallet.balance
        booking.total_amount -= wallet_used
        booking.remaining_amount = booking.total_amount

        wallet.balance = Decimal("0.00")

    wallet.save()

    WalletHistory.objects.create(
        user=booking.user,
        amount=wallet_used,
        transaction_type="debit",
        description=f"Wallet used for booking {booking.booking_id}"
    )

    booking.wallet_used = wallet_used
    booking.save()

    return booking











# def apply_wallet_to_booking(booking):
#     """
#     Deduct wallet balance for a booking
#     """

#     wallet = Wallet.objects.filter(user=booking.user).first()

#     if not wallet:
#         return booking

#     if wallet.balance <= 0:
#         return booking

#     wallet_used = Decimal("0.00")

#     #######################################################
#     # FULL WALLET PAYMENT
#     #######################################################

#     if wallet.balance >= booking.total_amount:

#         wallet_used = booking.total_amount
#         wallet.balance -= booking.total_amount

#         booking.total_amount = Decimal("0.00")
#         booking.remaining_amount = Decimal("0.00")

#     #######################################################
#     # PARTIAL WALLET PAYMENT
#     #######################################################

#     else:

#         wallet_used = wallet.balance

#         booking.total_amount -= wallet.balance
#         booking.remaining_amount = booking.total_amount

#         wallet.balance = Decimal("0.00")

#     #######################################################
#     # SAVE WALLET
#     #######################################################

#     wallet.save()

#     #######################################################
#     # SAVE WALLET HISTORY
#     #######################################################

#     WalletHistory.objects.create(
#         user=booking.user,
#         amount=wallet_used,
#         transaction_type="debit",
#         description=f"Wallet used for booking {booking.booking_id}"
#     )

#     #######################################################
#     # SAVE BOOKING
#     #######################################################

#     booking.wallet_used = wallet_used
#     booking.save()

#     return booking


from django.http import JsonResponse
from wallet.models import Wallet

def wallet_balance(request):

    if not request.user.is_authenticated:
        return JsonResponse({"balance": 0})

    wallet = Wallet.objects.filter(user=request.user).first()

    return JsonResponse({
        "balance": wallet.balance if wallet else 0
    })