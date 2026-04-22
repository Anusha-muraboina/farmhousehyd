from django.db import models

# Create your models here.






import random
import string
from decimal import Decimal
from django.urls import reverse
from django.db import models, transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import timedelta


from django.core.exceptions import ValidationError
from datetime import date

# bookings/models.py
from django.core.exceptions import ValidationError
from django.utils import timezone
from farmhouse.models import Farmhouse
from user.models import *
from django.conf import settings
from coupon.models import *

from django.utils import timezone
import pytz



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
    
    farmhouse = models.ForeignKey(  Farmhouse,  on_delete=models.CASCADE,  related_name="bookings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.SET_NULL,null=True, blank=True)
   
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
    address= models.TextField(null=True ,blank=True)
    special_requests = models.TextField(blank=True)
    wallet_used = models.DecimalField( max_digits=10, decimal_places=2, blank=True,null=True, default=0, help_text="Amount used from wallet for this booking")
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    disc_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tax_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_applied = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    check_out_time = models.TimeField( null=True, blank=True, help_text="Example: 09:00 AM")
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(  max_length=20,  choices=PAYMENT_METHOD_CHOICES)

    payment_status = models.CharField(  max_length=20,  choices=PAYMENT_STATUS_CHOICES, default='pending')

    status = models.CharField( max_length=20,  choices=STATUS_CHOICES, default='pending')

    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)

    confirmation_email_sent_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False , null=True,blank=True)
    cancelled_by = models.CharField(
        max_length=20,
        choices=[
            ("user", "User"),
            ("admin", "Admin"),
            ("farmhouse_owner","Farmhouse_owner"),
        ],
        null=True,
        blank=True
    )
    admin_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Manual discount by admin"
    )
    advance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Manual advance amount paid"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']



    # @property
    # def created_at_ist(self):
    #     if self.created_at:
    #         ist = pytz.timezone("Asia/Kolkata")
    #         return self.created_at.astimezone(ist)
    #     return None
    
    @property
    def advance_paid(self):

        if self.payment_status == "paid":
            return self.total_amount

        if self.payment_status == "partial":
            return (self.total_amount * Decimal("0.30")).quantize(Decimal("0.01"))

        return Decimal("0.00")



    def get_advance_paid(self):

        # Pay at farmhouse
        if self.payment_method == "farmhouse":
            return Decimal("0.00")

        # Partial payment
        if self.payment_method == "partial_razorpay":
            return (self.total_amount * Decimal("0.30")).quantize(Decimal("0.01"))

        # Full payment
        if self.payment_method == "full_razorpay":
            return self.total_amount

        return Decimal("0.00")
    
    def get_remaining_amount(self):

        advance = self.get_advance_paid()

        return self.total_amount - advance
    
    def send_booking_email(self, email_type,request=None):
        """
        email_type:
        pending / confirmed / cancelled / completed
        """

        templates = {
            "pending": {
                "user": "emails/booking_pending_user.html",
                "admin": "emails/booking_pending_user.html",
                "subject_user": "Booking Received – Awaiting Confirmation",
                "subject_admin": f"New Pending Booking - {self.booking_id}",
            },
            "confirmed": {
                "user": "emails/user_booking_email.html",
                "admin": "emails/admin_booking_email.html",
                "subject_user": "✅ Booking Confirmed – Farmhousehyd",
                "subject_admin": f"Booking Confirmed - {self.booking_id}",
            },
            "cancelled": {
                "user": "emails/booking_cancelled_user.html",
                "admin": "emails/booking_cancelled_user.html",
                "subject_user": "❌ Booking Cancelled",
                "subject_admin": f"Booking Cancelled - {self.booking_id}",
            },
            "completed": {
                "user": "emails/booking_completed_admin.html",
                "admin": "emails/booking_completed_user.html",
                "subject_user": "🎉 Stay Completed – Thank You!",
                "subject_admin": f"Stay Completed - {self.booking_id}",
            }
        }

        config = templates[email_type]

        # context = {"booking": self}
        ####################################
        # ⭐ Generate Invoice URL
        ####################################

        invoice_url = None


        try:
            invoice_path = reverse("view_invoice", args=[self.booking_id])
            invoice_url = f"https://farmhouseshyderabad.com{invoice_path}"   # 👉 change manually when needed
        except:
            invoice_url = None

        context = {
            "booking": self,
            "invoice_url": invoice_url
        }
        # USER EMAIL
        user_html = render_to_string(config["user"], context)

        user_email = EmailMultiAlternatives(
            subject=config["subject_user"],
            body="Booking update",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.guest_email],
        )

        user_email.attach_alternative(user_html, "text/html")
        user_email.send()

        # ADMIN EMAIL
        admin_html = render_to_string(config["admin"], context)

        admin_email = EmailMultiAlternatives(
            subject=config["subject_admin"],
            body="Booking update",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )

        admin_email.attach_alternative(admin_html, "text/html")
        admin_email.send()

    # ================= SAVE =================

    def save(self, *args, **kwargs):

        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_status = Booking.objects.get(pk=self.pk).status
            
        if not self.booking_id:
            self.booking_id = "FHH" + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

        ########################################
        # ✅ AUTO BLOCK DATES WHEN CONFIRMED
        ########################################

        # if (
        #     self.status == "confirmed"
        #     and old_status != "confirmed"
        # ):
        #     # BlockedDate.objects.get_or_create(
        #     #     farmhouse=self.farmhouse,
        #     #     start_date=self.check_in,
        #     #     end_date=self.check_out,
        #     #     defaults={
        #     #         "reason": f"Booking {self.booking_id}"
        #     #     }
        #     # )
            
        #     BlockedDate.objects.get_or_create(
        #         farmhouse=self.farmhouse,
        #         start_date=self.check_in,
        #         # ⭐ block only nights, NOT checkout day
        #         end_date=self.check_out - timedelta(days=1),
        #         defaults={
        #             "reason": f"Booking {self.booking_id}"
        #         }
        #     )
        # ✅ SEND EMAIL ONLY ONCE
        # if (
        #     self.status == "confirmed"
        #     and self.confirmation_email_sent_at is None
        #     and old_status != "confirmed"
        # ):
        #     transaction.on_commit(
        #         lambda: self.send_confirmation_email()
        #     )
        if is_new:
            # NEW BOOKING = pending email
            transaction.on_commit(
                lambda: self.send_booking_email("pending")
            )

        elif old_status != self.status:

            transaction.on_commit(
                lambda: self.send_booking_email(self.status)
            )
    # def save(self, *args, **kwargs):
    #     if not self.booking_id:
    #         import random, string
    #         self.booking_id = 'VFH' + ''.join(random.choices(string.digits, k=8))
    #     super().save(*args, **kwargs)

    def cancel_booking(self, user=None, reason=None, comment=None):

        if self.status == "cancelled":
            raise ValidationError("Booking already cancelled")

        if self.status == "completed":
            raise ValidationError("Completed booking cannot be cancelled")

        from datetime import timedelta
        from django.utils import timezone

        if self.check_in <= timezone.now().date() + timedelta(days=1):
            raise ValidationError("Free cancellation closed (within 24 hrs)")

        self.status = "cancelled"
        self.cancelled_at = timezone.now()
        self.cancelled_by = "user" if user else "admin"

        # unblock dates
        BlockedDate.objects.filter(
            farmhouse=self.farmhouse,
            start_date=self.check_in,
            end_date=self.check_out - timedelta(days=1)
        ).delete()

        if reason or comment:
            OrderCancelComment.objects.create(
                user=user,
                booking=self,
                reason=reason,
                comment=comment or ""
            )

        if self.payment_status == "paid":
            self.payment_status = "failed"

        ###################################
        # SAVE FIRST
        ###################################
        self.save()
        ###################################
        # SEND EMAIL AFTER DB COMMIT
        ###################################
        transaction.on_commit(
            lambda: self.send_booking_email("cancelled")
        )

    @property
    def nights(self):
        return (self.check_out - self.check_in).days

    def __str__(self):
        return f"{self.booking_id} - {self.guest_name}-{self.check_in} - {self.check_out} -{self.farmhouse}"


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
    # def clean(self):
    #     if self.start_date > self.end_date:
    #         raise ValidationError("End date must be after start date.")
    
    
    def clean(self):

        if not self.start_date or not self.end_date or not self.farmhouse:
            return

        # End must be after start
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be greater than start date.")

        if self.start_date < date.today():
            raise ValidationError("Cannot block past dates.")

        # ⭐ Exclusive overlap logic
        existing_blocks = BlockedDate.objects.filter(
            farmhouse=self.farmhouse
        ).exclude(pk=self.pk)

        for block in existing_blocks:
            if self.start_date < block.end_date and self.end_date > block.start_date:
                raise ValidationError(
                    f"Overlap with blocked range {block.start_date} → {block.end_date}"
                )

    # def clean(self):

    #     # ⭐ SAFETY CHECK FIRST
    #     if not self.start_date or not self.end_date:
    #         return

    #     # End must be after start
    #     if self.end_date <= self.start_date:
    #         raise ValidationError("End date must be greater than start date.")

    #     # Prevent past
    #     if self.start_date < date.today():
    #         raise ValidationError("Cannot block past dates.")
        
    #     overlaps = BlockedDate.objects.filter(
    #         farmhouse=self.farmhouse,
    #         start_date__lte=self.end_date,
    #         end_date__gte=self.start_date
    #     ).exclude(pk=self.pk)

    #     if overlaps.exists():
    #         raise ValidationError("These dates overlap with an existing blocked range.")

    def __str__(self):
        return f"Blocked: {self.start_date} → {self.end_date}"

class FarmhousePaymentPolicy(models.Model):

    farmhouse = models.OneToOneField(
        Farmhouse,
        on_delete=models.CASCADE,
        related_name="payment_policy"
    )

    allow_pay_at_farmhouse = models.BooleanField(default=False)
    allow_partial_payment = models.BooleanField(default=True)
    allow_full_payment = models.BooleanField(default=True)
    def __str__(self):
        return f"Blocked: {self.farmhouse} "
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
    def save(self, *args, **kwargs):

        if not self.invoice_id:
            self.invoice_id = "INV-" + ''.join(
                random.choices(string.digits, k=10)
            )

        super().save(*args, **kwargs)
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
    # def get_absolute_url(self):
    #     return reverse(
    #         "view_invoice",
    #         args=[self.booking.booking_id]
    #     )
    def __str__(self):
        return f"Cancellation - {self.booking.booking_id}"

