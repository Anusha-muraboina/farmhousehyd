# from django.db import models

# # Create your models here.

from django.db import models
from django.core.exceptions import ValidationError
class Banner(models.Model):
    title = models.CharField(max_length=200 ,null=True ,blank=True)
    image = models.ImageField(upload_to='banners/' , null=True , blank=True)
    link = models.URLField(blank=True ,null=True)
    is_active = models.BooleanField(default=True)
    Slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.title  or "banner" 


from django.db import models


class HomePopup(models.Model):

    image = models.ImageField(
        upload_to="popup/",
        help_text="Upload popup banner image"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "Homepage Popup"

class Location(models.Model):
    name = models.CharField(max_length=100)  # Gachibowli, Moinabad
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=255,blank=True,help_text="SEO title for search engines")
    meta_description = models.TextField( blank=True,help_text="Short description for SEO (150–160 chars)" )
    meta_keywords = models.CharField(max_length=255,blank=True, help_text="Comma separated keywords")
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    

class Amenity(models.Model):
    name = models.CharField(max_length=100)  # Swimming Pool, Lawn
    # icon = models.ImageField(upload_to='amenities/', blank=True, null=True)
    icon_class = models.CharField(
        max_length=100,
        help_text="Example: waves, bed, bath, car"
    )

    def __str__(self):
        return self.name

class FarmhouseFacilities(models.Model):
    name = models.CharField(max_length=100 ,null=True,blank=True)
    active = models.BooleanField(default=True)
    Slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.name




class Thingstocarry(models.Model):
    name = models.CharField(max_length=2000)
    active = models.BooleanField(default=True)
    slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.name



class Propertyrules(models.Model):
    name = models.CharField(max_length=2000)
    active = models.BooleanField(default=True)
    slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.name








from django.utils.text import slugify
from django.conf import settings
class Farmhouse(models.Model):
    
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="farmhouses",
        limit_choices_to={
            "is_staff": True
        },
        null=True,blank=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='farmhouses'
    )
    
    
    check_in_time = models.TimeField( default="14:00", help_text="Example: 2:00 PM" )
    check_out_time = models.TimeField( default="11:00",  help_text="Example: 11:00 AM")
    
    
    address = models.CharField(max_length=300)

    distance_km = models.PositiveIntegerField(
        help_text="Distance from city in KM (e.g. 21)"
    )
    
    halls = models.PositiveIntegerField(default=1)
    bedrooms = models.PositiveIntegerField(default=4)
    ac_bedrooms = models.PositiveIntegerField(default=4)

    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name='farmhouses'
    )
    facilities = models.ManyToManyField(
        FarmhouseFacilities,
        blank=True,
        related_name='farmhouses_facility'
    )

    properyrules =  models.ManyToManyField(
        Propertyrules,
        blank=True,
        related_name='propertyrules'
    )
    thingstocarry =  models.ManyToManyField(
        Thingstocarry,
        blank=True,
        related_name='thingstocarry'
    )
    
    short_description = models.TextField(
        help_text="Shown in card view"
    )

    description = models.TextField(
        help_text="Full farmhouse details page"
    )
    extra_guest_count = models.PositiveIntegerField(default=0)
    guest_count = models.PositiveIntegerField(default=20)

    free_cancellation = models.BooleanField(default=True)

    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    Slot_position = models.PositiveIntegerField(blank=True,null=True)
    meta_title = models.CharField(max_length=255,blank=True,help_text="SEO title for search engines")
    meta_description = models.TextField( blank=True,help_text="Short description for SEO (150–160 chars)" )
    meta_keywords = models.CharField(max_length=255,blank=True, help_text="Comma separated keywords")
    
    map_embed = models.TextField(
    blank=True,
    null=True,
    help_text="Paste Google Maps embed iframe"
    )
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10 ,
        null=True,blank=True
    )

    class Meta:
        ordering = ['-created_at']
    def get_price_by_date(self, date):
        """
        date → datetime.date
        """
        pricing = self.pricing

    #  SALE PRICE ALWAYS WINS
        if pricing.sale_price and pricing.sale_price > 0:
            return pricing.sale_price

        weekday = date.weekday()  # Monday=0, Sunday=6

        if weekday >= 5:  # Saturday, Sunday
            return self.pricing.weekend_price

        return self.pricing.normal_day_price
    
    def get_location(self, obj):
        if obj.location:
            return {
                "name": obj.location.name,
                "slug": obj.location.slug
            }
        return None
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        
        
        if not self.pk and self.user and self.user.farmhouse_user:

            limit = self.user.farmhouse_limit
            current = Farmhouse.objects.filter(user=self.user).count()

            if current >= limit:
                raise ValidationError(
                    f"This owner can only create {limit} farmhouses."
                )

        # if not self.pk and self.user:

        #     # Only check for farmhouse owners
        #     if self.user.farmhouse_user:

        #         limit = self.user.farmhouse_limit

        #         current_count = Farmhouse.objects.filter(user=self.user).count()

        #         if current_count >= limit:
        #             raise ValidationError(
        #                 f"This owner can only create {limit} farmhouses."
        #             )

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class FarmhousePricing(models.Model):
    DAY_TYPE_CHOICES = (
        ('normal', 'Normal Day'),
        ('weekend', 'Weekend'),
    )

    farmhouse = models.OneToOneField(
        Farmhouse,
        on_delete=models.CASCADE,
        related_name='pricing'
    )
    # 
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional sale price. Overrides all prices."
    )
    normal_day_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monday to Friday price"
    )

    weekend_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Saturday & Sunday price"
    )

    extra_guest_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Price per extra guest (optional)"
    )

    def __str__(self):
        return f"{self.farmhouse.title} Pricing"






class FarmhouseImage(models.Model):
    farmhouse = models.ForeignKey(
        Farmhouse,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='farmhouses/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.farmhouse.title



class TouristPlace(models.Model):
    title = models.CharField(
        max_length=150,
        help_text="Example: Ramoji Film City"
    )

    image = models.ImageField(
        upload_to="tourist_places/",
        help_text="Upload place image"
    )

    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Example: 0 Tour / Nearby Attraction"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tourist Place"
        verbose_name_plural = "Tourist Places"

    def __str__(self):
        return self.title

