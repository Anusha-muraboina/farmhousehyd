from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


# class Coupon(models.Model):
#     DISCOUNT_TYPE_CHOICES = (
#         ('percentage', 'Percentage'),
#         ('fixed', 'Fixed Amount'),
#     )

#     code = models.CharField(
#         max_length=50,
#         unique=True,
#         help_text="Example: NEWYEAR50"
#     )

#     discount_type = models.CharField(
#         max_length=20,
#         choices=DISCOUNT_TYPE_CHOICES
#     )

#     discount_value = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         help_text="Percentage (e.g. 10) or fixed amount (e.g. 500)"
#     )

#     min_order_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0,
#         help_text="Minimum order value to apply coupon"
#     )

#     max_discount_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         help_text="Maximum discount limit (for percentage coupons)"
#     )

#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()

#     usage_limit = models.PositiveIntegerField(
#         null=True,
#         blank=True,
#         help_text="How many times coupon can be used"
#     )

#     used_count = models.PositiveIntegerField(default=0)

#     is_active = models.BooleanField(default=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.code

#     def is_valid(self, order_amount):
#         now = timezone.now()

#         if not self.is_active:
#             return False

#         if now < self.valid_from or now > self.valid_to:
#             return False

#         if self.usage_limit and self.used_count >= self.usage_limit:
#             return False

#         if order_amount < self.min_order_amount:
#             return False

#         return True

#     def calculate_discount(self, order_amount):
#         if self.discount_type == 'percentage':
#             discount = (order_amount * self.discount_value) / 100
#             if self.max_discount_amount:
#                 discount = min(discount, self.max_discount_amount)
#             return discount

#         return min(self.discount_value, order_amount)
