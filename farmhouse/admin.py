from django.contrib import admin
from .models import *
# Register your models here.
class FarmhousePricingInline(admin.StackedInline):
    model = FarmhousePricing
    can_delete = False


@admin.register(Farmhouse)
class FarmhouseAdmin(admin.ModelAdmin):
    inlines = [FarmhousePricingInline]


