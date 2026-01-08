from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from user.models import *
from farmhouse.models import *
# Create your models here.

from django.db import models
from django.utils import timezone
from decimal import Decimal


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('flat', 'Flat Amount'),
        ('percentage', 'Percentage'),
    )

    title = models.CharField(
        max_length=150,
        help_text="Example: New Year Coupon"
    )

    code = models.CharField(
        max_length=30,
        unique=True,
        help_text="Example: NEWYEAR30"
    )

    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="20 = 20% | 1500 = ₹1500"
    )

    min_booking_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00")
    )

    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Only for percentage coupons"
    )

    start_date = models.DateField()
    end_date = models.DateField()

    usage_limit = models.PositiveIntegerField(
        default=0,
        help_text="0 = Unlimited usage"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


    # ✅ Check coupon validity
    def is_valid(self):
        today = timezone.now().date()
        return self.is_active and self.start_date <= today <= self.end_date

    # ✅ Calculate discount
    def calculate_discount(self, amount):
        if amount < self.min_booking_amount:
            return Decimal("0.00")

        if self.discount_type == 'percentage':
            discount = (amount * self.discount_value) / Decimal("100")
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return discount

        return min(self.discount_value, amount)
    def __str__(self):
        return f"{self.title} ({self.code})"

class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usage_count = models.PositiveIntegerField(default=0)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" used {self.coupon.coupon} on {self.used_at}"





















