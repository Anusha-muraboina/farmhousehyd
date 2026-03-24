from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Wallet(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # connects to your custom User
        on_delete=models.CASCADE,
        related_name="wallet"
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
        # ✅ NEW FIELDS
    # start_date = models.DateTimeField(
    #     auto_now_add=True,
    #     help_text="Wallet activation date"
    # )

    # expiry_date = models.DateTimeField(
    #     null=True,
    #     blank=True,
    #     help_text="Wallet expiry date"
    # )
    wallet_start_date = models.DateField()
    wallet_end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    def is_expired(self):
        from django.utils import timezone
        return self.wallet_end_date and timezone.now() > self.wallet_end_date

    def __str__(self):
        return f"{self.user.username} - ₹{self.balance}"
    
    
class WalletHistory(models.Model):

    TRANSACTION_TYPE = [
        ("credit", "Credit"),
        ("debit", "Debit"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet_transactions"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₹{self.amount}"
    
    
    
    