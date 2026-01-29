from django.db import models

# Create your models here.
from django.db import models
from ckeditor.fields import RichTextField

class Choos_Services(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    icon = models.CharField(  max_length=100,   blank=True, help_text="Example: fa-solid fa-house or lucide-home" )
    image = models.ImageField(upload_to='chosse_banners/',null=True ,blank=True)
    is_active = models.BooleanField(default=True)
    Slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.title

from django.db import models

class Facilities(models.Model):
    name =  models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
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
    image = models.ImageField(upload_to='chosse_banners/',null=True ,blank=True)
    is_active = models.BooleanField(default=True)
    Slot_position = models.PositiveIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.title




class AboutSection(models.Model):
    title_tag = models.CharField(
        max_length=50,
        default="About Us",
        help_text="Small green label text"
    )

    main_title = models.CharField(
        max_length=200,
        help_text="Big heading text"
    )

    description = RichTextField(
        help_text="You can add HTML tags, lists, bold, etc."
    )

    image = models.ImageField(
        upload_to="about/images/",
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to="about/videos/",
        blank=True,
        null=True,
        help_text="Upload mp4 video"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.main_title


class AboutFeature(models.Model):

    about = models.ForeignKey(
        AboutSection,
        on_delete=models.CASCADE,
        related_name="features"
    )

    icon = models.CharField(
        max_length=100,
        help_text="Example: fa-solid fa-house or hero-home",
        null=True,
        blank=True
    )


    title = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title









# in home know who we are models
class AboutWhoWeAre(models.Model):
    # Headings
    small_title = models.CharField(
        max_length=100,
        default="About Us"
    )

    main_title = models.CharField(
        max_length=200,
        default="Know Who We Are"
    )

    # Mission & Vision
    mission_title = models.CharField(
        max_length=200,
        default="Mission & Vision"
    )

    mission_description = models.TextField()

    # How we do it differently
    difference_title = models.CharField(
        max_length=200,
        default="How We Do It Differently"
    )

    difference_description = models.TextField()

    # Image
    image = models.ImageField(
        upload_to="about/",
        help_text="Main About Section Image"
    )
    # Button
    button_text = models.CharField(
        max_length=50,
        default="More about us"
    )

    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Know About Section"
        verbose_name_plural = "Know About Section"

    def __str__(self):
        return self.main_title


# give me the crud for the with pagination for admin dashbaord it is under cms main section give me CRUD
