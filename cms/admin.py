from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import *

admin.site.register(WhoWeAre)
admin.site.register(OurFacility)
admin.site.register(Facilities)
admin.site.register(Choos_Services)

class AboutFeatureInline(admin.TabularInline):
    model = AboutFeature
    extra = 4


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    inlines = [AboutFeatureInline]
    list_display = ("main_title", "is_active")
