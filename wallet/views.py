from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def wallet(request):
    return HttpResponse("Hello, this is Blog Page")
    # return render(request , "contact.html")



from wallet.models import Wallet, WalletHistory


def add_wallet_credit(user, amount, description="Admin wallet credit"):

    wallet, created = Wallet.objects.get_or_create(user=user)

    wallet.balance += amount
    wallet.save()

    WalletHistory.objects.create(
        user=user,
        amount=amount,
        transaction_type="credit",
        description=description
        
    )
    
from wallet.models import Wallet, WalletHistory


def apply_wallet_to_booking(booking):

    wallet = Wallet.objects.filter(user=booking.user).first()

    if not wallet or wallet.balance <= 0:
        return booking

    wallet_used = 0

    if wallet.balance >= booking.total_amount:

        wallet_used = booking.total_amount
        wallet.balance -= booking.total_amount
        booking.total_amount = 0

    else:

        wallet_used = wallet.balance
        booking.total_amount -= wallet.balance
        wallet.balance = 0

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