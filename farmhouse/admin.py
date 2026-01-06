from django.contrib import admin
from .models import *

class FarmhousePricingInline(admin.StackedInline):
    model = FarmhousePricing
    can_delete = False
    extra = 0

class FarmhouseImageInline(admin.TabularInline):
    model = FarmhouseImage
    extra = 1

@admin.register(Farmhouse)
class FarmhouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'user', 'price_per_day', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'location', 'user')
    search_fields = ('title', 'address', 'user__username', 'user__email')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FarmhousePricingInline, FarmhouseImageInline]
    filter_horizontal = ('amenities',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'user', 'location', 'address', 'distance_km')
        }),
        ('Property Details', {
            'fields': ('halls', 'bedrooms', 'ac_bedrooms', 'amenities')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing & Status', {
            'fields': ('price_per_day', 'free_cancellation', 'is_active', 'is_featured')
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter user field to show only users with assignedpermission=True"""
        if db_field.name == "user":
            from user.models import User
            kwargs["queryset"] = User.objects.filter(assignedpermission=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        """Auto-assign current user as user if not set"""
        if not obj.user and request.user.assignedpermission:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'Slot_position')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'Slot_position')

@admin.register(FarmhousePricing)
class FarmhousePricingAdmin(admin.ModelAdmin):
    list_display = ('farmhouse', 'normal_day_price', 'weekend_price', 'extra_guest_price')
    search_fields = ('farmhouse__title',)

@admin.register(FarmhouseImage)
class FarmhouseImageAdmin(admin.ModelAdmin):
    list_display = ('farmhouse', 'image', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('farmhouse__title',)
