# farmhouse/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Farmhouse, FarmhousePricing, FarmhouseImage ,Thingstocarry ,Propertyrules
from .models import *


User = get_user_model()


class FarmhousePricingInline(admin.StackedInline):
    model = FarmhousePricing
    can_delete = False
    extra = 0


admin.site.register(Thingstocarry)
admin.site.register(Propertyrules)
admin.site.register(HomePopup)


class FarmhouseImageInline(admin.TabularInline):
    model = FarmhouseImage
    extra = 1



@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("is_active",)
    search_fields = ("name",)
    fields = (
        "name",
        "slug",
        "is_active",
        "meta_title",
        "meta_description",
        "meta_keywords",
    )

@admin.register(Farmhouse)
class FarmhouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'user', 'price_per_day','check_in_time', 'check_out_time', 'Slot_position', 'map_embed','is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'location', 'user')
    search_fields = ('title', 'address', 'user__username', 'user__email')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FarmhousePricingInline, FarmhouseImageInline]
    # filter_horizontal = ('amenities')
    filter_horizontal = ('amenities', 'facilities','properyrules','thingstocarry')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'user', 'location', 'address','guest_count','extra_guest_count' , 'Slot_position','map_embed' ,'check_in_time', 'check_out_time', 'distance_km')
        }),
        ('Property Details', {
            'fields': ('halls', 'bedrooms', 'ac_bedrooms', 'amenities','facilities',  'properyrules','thingstocarry')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing & Status', {
            'fields': ('price_per_day', 'free_cancellation', 'is_active', 'is_featured')
        }),
        
                # ⭐ NEW SEO SECTION
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'description': 'Meta tags used for search engines (Google SEO)'
        }),

    )

    # ✅ ONLY farmhouse_user = True USERS
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(
                farmhouse_user=True,
                is_staff= True,
                 is_superuser=False,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # ✅ SINGLE save_model (no duplicates)
    def save_model(self, request, obj, form, change):
        # Staff admin → auto-assign himself
        if not request.user.is_superuser:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Amenity)
admin.site.register(Banner)
admin.site.register(FarmhouseFacilities)


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    
    
