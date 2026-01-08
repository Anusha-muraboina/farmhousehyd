from django.db import models

# Create your models here.










# bookings/models.py
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from farmhouse.models import Farmhouse
from user.models import *
from django.conf import settings
from coupon.models import *



class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('farmhouse', 'Pay at Farmhouse'),
        ('partial_razorpay', 'Pay 30% via Razorpay'),
        ('full_razorpay', 'Full Payment via Razorpay'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)

    farmhouse = models.ForeignKey(
        Farmhouse,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    # Guest snapshot (VERY IMPORTANT)
    guest_name = models.CharField(max_length=200)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=15)

    guest_count = models.PositiveIntegerField(default=20)
    extra_guest_count = models.PositiveIntegerField(default=0)

    check_in = models.DateField()
    check_out = models.DateField()
    check_in_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Example: 10:00 AM"
    )
    special_requests = models.TextField(blank=True)

    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    disc_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tax_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_applied = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    check_out_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Example: 09:00 AM"
    )
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)



    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_id:
            import random, string
            self.booking_id = 'VFH' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    @property
    def nights(self):
        return (self.check_out - self.check_in).days

    def __str__(self):
        return f"{self.booking_id} - {self.guest_name}"



# models.py
class BlockedDate(models.Model):
    farmhouse = models.ForeignKey(
        Farmhouse,
        on_delete=models.CASCADE,
        related_name="blocked_dates"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")

        overlaps = BlockedDate.objects.filter(
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(pk=self.pk)

        if overlaps.exists():
            raise ValidationError("These dates overlap with an existing blocked range.")

    def __str__(self):
        return f"Blocked: {self.start_date} → {self.end_date}"


class Invoice(models.Model):
    invoice_id = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField(auto_now_add=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="invoice"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice_id


class CancelReason(models.Model):
    reason = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.reason


class OrderCancelComment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="cancellation_comments"
    )

    reason = models.ForeignKey(
        CancelReason,
        on_delete=models.SET_NULL,
        null=True
    )

    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancellation - {self.booking.booking_id}"

