from django import forms
from farmhouse.models import *


# class FarmhouseForm(forms.ModelForm):
#     class Meta:
#         model = Farmhouse
#         fields = [
#             "title",
#             "location",
#             "address",
#             "distance_km",
#             "halls",
#             "bedrooms",
#             "ac_bedrooms",
#             "amenities",
#             "short_description",
#             "description",
#             "price_per_day",
#             "free_cancellation",
#             "is_active",
#             "is_featured",
#         ]

#         widgets = {
#             "amenities": forms.CheckboxSelectMultiple(),
#             "description": forms.Textarea(attrs={"rows": 5}),
#             "short_description": forms.Textarea(attrs={"rows": 3}),
#         }

from django import forms
# from .models import Farmhouse, FarmhousePricing


# ✅ PERFECT TAILWIND INPUT STYLE
INPUT_CLASS = (
    "w-full px-4 py-3 border border-gray-300 rounded-xl "
    "bg-white text-gray-800 "
    "focus:outline-none focus:ring-2 focus:ring-orange-400 "
    "focus:border-orange-400 transition"
)

TEXTAREA_CLASS = (
    "w-full px-4 py-3 border border-gray-300 rounded-xl "
    "bg-white text-gray-800 resize-none "
    "focus:outline-none focus:ring-2 focus:ring-orange-400 "
    "focus:border-orange-400 transition"
)


class FarmhouseForm(forms.ModelForm):
    class Meta:
        model = Farmhouse
        fields = [
            "title",
            "user",
            "location",
            "address",
            "distance_km",
            "halls",
            "bedrooms",
            "ac_bedrooms",
            "amenities",
            "short_description",
            "description",
            "price_per_day",
            "free_cancellation",
            "is_active",
            "is_featured",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "user": forms.Select(attrs={"class": INPUT_CLASS}),
            "location": forms.Select(attrs={"class": INPUT_CLASS}),
            "address": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "distance_km": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "halls": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "bedrooms": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "ac_bedrooms": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "price_per_day": forms.NumberInput(attrs={"class": INPUT_CLASS}),

            "short_description": forms.Textarea(
                attrs={"class": TEXTAREA_CLASS, "rows": 3}
            ),
            "description": forms.Textarea(
                attrs={"class": TEXTAREA_CLASS, "rows": 6}
            ),

            "amenities": forms.CheckboxSelectMultiple(
                attrs={"class": "space-y-2"}
            ),
        }


class FarmhousePricingForm(forms.ModelForm):
    class Meta:
        model = FarmhousePricing
        fields = [
            "normal_day_price",
            "weekend_price",
            "extra_guest_price",
        ]

        widgets = {
            "normal_day_price": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "weekend_price": forms.NumberInput(attrs={"class": INPUT_CLASS}),
            "extra_guest_price": forms.NumberInput(attrs={"class": INPUT_CLASS}),
        }


# class FarmhousePricingForm(forms.ModelForm):
#     class Meta:
#         model = FarmhousePricing
#         fields = [
#             "normal_day_price",
#             "weekend_price",
#             "extra_guest_price",
#         ]


class FarmhouseImageForm(forms.ModelForm):
    class Meta:
        model = FarmhouseImage
        fields = ["image", "is_primary"]
        widgets = {
            # "image": forms.ImageField(attrs={"class": INPUT_CLASS})
        }
        
        
        
        
# 

from django import forms
from superadmin_dashboard.models import *

INPUT = "w-full border px-4 py-3 rounded-xl focus:ring-2 focus:ring-orange-400"

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT}),
            "link": forms.URLInput(attrs={"class": INPUT}),
            "Slot_position": forms.NumberInput(attrs={"class": INPUT}),
            "is_active": forms.CheckboxInput(attrs={"class": "w-5 h-5"}),
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT}),
            "slug": forms.TextInput(attrs={"class": INPUT}),
            "is_active": forms.CheckboxInput(attrs={"class": "w-5 h-5"}),
        }


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT}),
            "icon_class": forms.TextInput(attrs={"class": INPUT}),
        }



# cms

from django import forms
from cms.models import *

# class ChooseServiceForm(forms.ModelForm):
#     class Meta:
#         model = Choos_Services
#         fields = "__all__"


# class FacilityForm(forms.ModelForm):
#     class Meta:
#         model = Facilities
#         fields = "__all__"


# class OurFacilityForm(forms.ModelForm):
#     class Meta:
#         model = OurFacility
#         fields = "__all__"
#         widgets = {
#             "facilities": forms.CheckboxSelectMultiple()
#         }


# class WhoWeAreForm(forms.ModelForm):
#     class Meta:
#         model = WhoWeAre
#         fields = "__all__"


# class AboutSectionForm(forms.ModelForm):
#     class Meta:
#         model = AboutSection
#         fields = "__all__"


# class AboutFeatureForm(forms.ModelForm):
#     class Meta:
#         model = AboutFeature
#         fields = "__all__"


# class AboutWhoWeAreForm(forms.ModelForm):
#     class Meta:
#         model = AboutWhoWeAre
#         fields = "__all__"


from django import forms
from .models import *

TAILWIND_INPUT = "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
TAILWIND_TEXTAREA = "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
TAILWIND_CHECKBOX = "mr-2"
TAILWIND_FILE = "w-full border rounded-md p-2 bg-white"

class ChooseServiceForm(forms.ModelForm):
    class Meta:
        model = Choos_Services
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "description": forms.Textarea(attrs={"class": TAILWIND_TEXTAREA, "rows": 4}),
            "icon": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "image": forms.ClearableFileInput(attrs={"class": TAILWIND_FILE}),
            "Slot_position": forms.NumberInput(attrs={"class": TAILWIND_INPUT}),
        }


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facilities
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
        }


class OurFacilityForm(forms.ModelForm):
    class Meta:
        model = OurFacility
        fields = "__all__"
        widgets = {
            "main_title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "description": forms.Textarea(attrs={"class": TAILWIND_TEXTAREA, "rows": 4}),
            "image": forms.ClearableFileInput(attrs={"class": TAILWIND_FILE}),
            "facilities": forms.CheckboxSelectMultiple(
                attrs={"class": "space-y-2"}
            ),
        }


class WhoWeAreForm(forms.ModelForm):
    class Meta:
        model = WhoWeAre
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "description": forms.Textarea(attrs={"class": TAILWIND_TEXTAREA, "rows": 4}),
            "icon": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "image": forms.ClearableFileInput(attrs={"class": TAILWIND_FILE}),
            "Slot_position": forms.NumberInput(attrs={"class": TAILWIND_INPUT}),
        }


class AboutSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = "__all__"
        widgets = {
            "title_tag": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "main_title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "description": forms.Textarea(attrs={"class": TAILWIND_TEXTAREA, "rows": 6}),
            "image": forms.ClearableFileInput(attrs={"class": TAILWIND_FILE}),
            "video": forms.ClearableFileInput(attrs={"class": TAILWIND_FILE}),
        }


class AboutFeatureForm(forms.ModelForm):
    class Meta:
        model = AboutFeature
        fields = "__all__"
        widgets = {
            "about": forms.Select(attrs={"class": TAILWIND_INPUT}),
            "icon": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
        }


class AboutWhoWeAreForm(forms.ModelForm):
    class Meta:
        model = AboutWhoWeAre
        fields = "__all__"
        widgets = {
            "small_title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "main_title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "mission_title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "mission_description": forms.Textarea(attrs={"class": TAILWIND_TEXTAREA, "rows": 4}),
            "difference_title": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
            "difference_description": forms.Textarea(attrs={"class": TAILWIND_TEXTAREA, "rows": 4}),
            "image": forms.ClearableFileInput(attrs={"class": TAILWIND_FILE}),
            "button_text": forms.TextInput(attrs={"class": TAILWIND_INPUT}),
        }





# coupon

from django import forms
from coupon.models import Coupon

TAILWIND = "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": TAILWIND}),
            "code": forms.TextInput(attrs={"class": TAILWIND}),
            "discount_type": forms.Select(attrs={"class": TAILWIND}),
            "discount_value": forms.NumberInput(attrs={"class": TAILWIND}),
            "min_booking_amount": forms.NumberInput(attrs={"class": TAILWIND}),
            "max_discount_amount": forms.NumberInput(attrs={"class": TAILWIND}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": TAILWIND}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": TAILWIND}),
            "usage_limit": forms.NumberInput(attrs={"class": TAILWIND}),
        }
