from django.db import models

# Create your models here.

class Choos_Services(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    icon = models.CharField(  max_length=100,   blank=True, help_text="Example: fa-solid fa-house or lucide-home" )
    image = models.ImageField(upload_to='chosse_banners/')
    is_active = models.BooleanField(default=True)
    Slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.title

from django.db import models

class Facilities(models.Model):
    name =  models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

class OurFacility(models.Model):
    facilities = models.ManyToManyField(Facilities , blank=True, related_name='our_facilities')
    main_title = models.CharField(   max_length=200,      help_text="Example: Finest Farmhouses with Food"  )
    description = models.TextField(    help_text="Short paragraph description")
    image = models.ImageField(    upload_to='our_specialty/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.main_title

class WhoWeAre(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    icon = models.CharField(  max_length=100,   blank=True, help_text="Example: fa-solid fa-house or lucide-home" )
    image = models.ImageField(upload_to='chosse_banners/')
    is_active = models.BooleanField(default=True)
    Slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.title
