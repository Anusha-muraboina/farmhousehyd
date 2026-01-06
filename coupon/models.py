# from django.db import models

# # Create your models here.
# from django.db import models
# from django.conf import settings
# from user.models import *
# from product.models import *
# # Create your models here.

# class Coupon(models.Model):
#     DISCOUNT_TYPE_CHOICES = [
#         ('fixed_amount', 'Fixed Amount'),
#         ('percentage', 'Percentage'),
#     ]

#     coupon = models.CharField(max_length=50, unique=True)
#     description = models.TextField()
#     discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
#     coupon_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     allow_free_shipping = models.BooleanField(default=False)
#     coupon_start_date = models.DateField()
#     coupon_end_date = models.DateField()
#     minimum_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     maximum_spend = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     individual_use_only = models.BooleanField(default=False)
#     exclude_sale_items = models.BooleanField(default=False)
#     products = models.ManyToManyField(Product, related_name='coupon_products', blank=True)
#     exclude_products = models.ManyToManyField(Product, related_name='excluded_coupon_products', blank=True)
#     product_categories = models.ManyToManyField(ParentCategory, related_name='coupon_product_categories', blank=True)
#     exclude_categories = models.ManyToManyField(ParentCategory, related_name='excluded_coupon_categories', blank=True)
#     allowed_emails = models.TextField(blank=True)
#     usage_limit_per_coupon = models.PositiveIntegerField(default=0, blank=True, null=True)
#     limit_usage_to_x_items = models.PositiveIntegerField(default=0, blank=True, null=True)
#     usage_limit_per_user = models.PositiveIntegerField(default=0, blank=True, null=True)

#     def __str__(self):
#         return self.coupon

# class CouponUsage(models.Model):
#     coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     usage_count = models.PositiveIntegerField(default=0)
#     used_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f" used {self.coupon.coupon} on {self.used_at}"





















