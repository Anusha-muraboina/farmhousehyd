from django.contrib import admin

# Register your models here.
from .models import Wallet, WalletHistory



@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance", "created_at")


@admin.register(WalletHistory)
class WalletHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "transaction_type", "created_at")
   
