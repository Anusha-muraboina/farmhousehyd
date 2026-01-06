from django.db import models

# Create your models here.











# class Booking(models.Model):
#     """Guest bookings"""
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('cancelled', 'Cancelled'),
#         ('completed', 'Completed'),
#     ]
#     PAYMENT_METHOD_CHOICES = [
#         ('farmhouse', 'Pay at Farmhouse'),               # no online payment
#         ('partial_razorpay', 'Pay 30% via Razorpay'),    # 30% online, 70% later
#         ('full_razorpay', 'Full Payment via Razorpay'),  # 100% online
#     ]

#     PAYMENT_STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('partial','partial'),
#         ('paid', 'Paid'),
#         ('failed', 'Failed'),
#     ]

#     booking_id = models.CharField(max_length=20, unique=True, editable=False)
#     # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)

#     guest_name = models.CharField(max_length=200)
#     guest_email = models.EmailField()
#     guest_phone = models.CharField(max_length=15)
#     guest_count = models.IntegerField(default=15)
#     extra_guest_count = models.IntegerField(default=0 ,null=True ,blank=True)
    
#     check_in = models.DateField()
#     check_in_time = models.TimeField(null=True, blank=True)
#     check_out = models.DateField()
#     check_out_time = models.TimeField(null=True, blank=True)

#     special_requests = models.TextField(blank=True)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     sub_total = models.DecimalField(max_digits=10, decimal_places=2 ,null=True,blank=True)
#     remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     tax_price = models.DecimalField(max_digits=10, decimal_places=2 ,null=True,blank=True)
#     # offer_applied = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
#     # coupon_applied = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
#     disc_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
#     cancellation_reason = models.TextField(blank=True, null=True)
#     payment_method = models.CharField(
#         max_length=20,
#         choices=PAYMENT_METHOD_CHOICES,
#         default='farmhouse'
#     )
#     transaction_id = models.CharField(max_length=100, blank=True, null=True)
#     payment_id = models.CharField(max_length=100, blank=True, null=True)    
#     payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)

#     updated_at = models.DateTimeField(auto_now=True)

#     # class Meta:
#     #     ordering = ['-created_at']
#     class Meta:
#         ordering = ['-created_at']
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["guest_email", "check_in", "check_out", "payment_method"],
#                 name="unique_booking_guest_dates"
#             )
#         ]
#     def save(self, *args, **kwargs):
#         if not self.booking_id:
#             import random
#             import string
#             self.booking_id = 'VFH' + ''.join(random.choices(string.digits, k=8))
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.booking_id} - {self.guest_name}"

#     @property
#     def num_nights(self):
#         return (self.check_out - self.check_in).days
#     @property
#     def final_total(self):
#         return (self.sub_total or 0) - (self.disc_price or 0)



# class Invoice(models.Model):
#     invoice_id = models.CharField(max_length=50)
#     invoice_date = models.DateField()
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     Active = models.BooleanField(default=False)

#     def __str__(self):
#         return self.invoice_id

# class cancel_reason(models.Model):
#     reason = models.CharField(max_length=255)
#     Active = models.BooleanField(default=False)

#     def __str__(self):
#         return self.reason

# class order_cancel_comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user
#     order = models.ForeignKey(Order, on_delete=models.CASCADE) # Order Of Cancellation
#     reason = models.ForeignKey(cancel_reason, on_delete=models.CASCADE) # Reason Of Cancellation
#     comment = models.TextField()  # Comment Of Cancellation
#     timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of cancellation

#     def __str__(self):
#         return f"Order #{self.order.id} Cancellation"
