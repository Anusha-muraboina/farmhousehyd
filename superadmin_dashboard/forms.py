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
