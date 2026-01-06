# from django.db import models

# # Create your models here.

from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True ,null=True)
    is_active = models.BooleanField(default=True)
    Slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.title









class Location(models.Model):
    name = models.CharField(max_length=100)  # Gachibowli, Moinabad
    slug = models.SlugField(unique=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


class Amenity(models.Model):
    name = models.CharField(max_length=100)  # Swimming Pool, Lawn
    icon = models.ImageField(upload_to='amenities/', blank=True, null=True)

    def __str__(self):
        return self.name


from django.utils.text import slugify



class Farmhouse(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='farmhouses'
    )

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

    short_description = models.TextField(
        help_text="Shown in card view"
    )

    description = models.TextField(
        help_text="Full farmhouse details page"
    )

    free_cancellation = models.BooleanField(default=True)

    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    def get_price_by_date(self, date):
        """
        date → datetime.date
        """
        weekday = date.weekday()  # Monday=0, Sunday=6

        if weekday >= 5:  # Saturday, Sunday
            return self.pricing.weekend_price

        return self.pricing.normal_day_price
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
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
