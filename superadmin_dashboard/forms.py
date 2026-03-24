from django import forms
from farmhouse.models import *



from booking.models import FarmhousePaymentPolicy
from farmhouse.models import Location
from farmhouse.models import FarmhouseFacilities
from booking.models import CancelReason


class FarmhousePaymentPolicyForm(forms.ModelForm):
    class Meta:
        model = FarmhousePaymentPolicy
        fields = "__all__"

        widgets = {
            "farmhouse": forms.Select(attrs={"class": "form-select"}),
            "allow_pay_at_farmhouse": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "allow_partial_payment": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "allow_full_payment": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }





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
# form-control-lg
INPUT_CLASS = "form-control "
TEXTAREA_CLASS = "form-control "


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class FarmhouseForm(forms.ModelForm):

    class Meta:
        model = Farmhouse
        fields = "__all__"

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "user": forms.Select(attrs={"class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "distance_km": forms.NumberInput(attrs={"class": "form-control"}),
            "halls": forms.NumberInput(attrs={"class": "form-control"}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-control"}),
            "ac_bedrooms": forms.NumberInput(attrs={"class": "form-control"}),
            "short_description": forms.Textarea(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "price_per_day": forms.NumberInput(attrs={"class": "form-control"}),
            "free_cancellation": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "map_embed" :  forms.TextInput(attrs={"class": "form-control"}),
            
                                    # ✅ Slot Position
            "Slot_position": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter slot position"
            }),
                        # ✅ Check-in / Check-out time
            "check_in_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "check_out_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            
            
            
                        # ✅ ADD THESE
            "guest_count": forms.NumberInput(attrs={"class": "form-control"}),
            "extra_guest_count": forms.NumberInput(attrs={"class": "form-control"}),
            "commission_percentage": forms.NumberInput(attrs={"class": "form-control"}),
            
            "meta_title": forms.TextInput(attrs={"class": "form-control"}),
            "meta_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "meta_keywords": forms.TextInput(attrs={"class": "form-control"}),
            
                        # ✅ ManyToMany with multi select
            # "amenities": forms.SelectMultiple(attrs={"class": "form-control"}),
            # "thingstocarry": forms.SelectMultiple(attrs={"class": "form-control"}),
            # "properyrules": forms.SelectMultiple(attrs={"class": "form-control"}),

    "amenities": forms.CheckboxSelectMultiple(),
    "thingstocarry": forms.CheckboxSelectMultiple(),
    "properyrules": forms.CheckboxSelectMultiple(),
    "facilities": forms.CheckboxSelectMultiple(),
    "breakfast_dinner_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
    
    
    
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Only farmhouse owners
        self.fields["user"].queryset = User.objects.filter(farmhouse_user=True)
        
        
        
        
        
        
# class FarmhouseForm(forms.ModelForm):
#     class Meta:
#         model = Farmhouse
#         fields = "__all__"

#         widgets = {
#             "title": forms.TextInput(attrs={
#                 "class": INPUT_CLASS,
#                 "placeholder": "Enter farmhouse title"
#             }),

#             "location": forms.Select(attrs={
#                 "class": INPUT_CLASS
#             }),

#             "address": forms.TextInput(attrs={
#                 "class": INPUT_CLASS,
#                 "placeholder": "Enter full address"
#             }),

#             "distance_km": forms.NumberInput(attrs={
#                 "class": INPUT_CLASS
#             }),

#             "halls": forms.NumberInput(attrs={
#                 "class": INPUT_CLASS
#             }),

#             "bedrooms": forms.NumberInput(attrs={
#                 "class": INPUT_CLASS
#             }),

#             "ac_bedrooms": forms.NumberInput(attrs={
#                 "class": INPUT_CLASS
#             }),

#             "short_description": forms.Textarea(attrs={
#                 "class": TEXTAREA_CLASS,
#                 "rows": 3
#             }),

#             "description": forms.Textarea(attrs={
#                 "class": TEXTAREA_CLASS,
#                 "rows": 6
#             }),

#             "price_per_day": forms.NumberInput(attrs={
#                 "class": INPUT_CLASS
#             }),

#             "free_cancellation": forms.CheckboxInput(attrs={
#                 "class": "form-check-input"
#             }),

#             "is_active": forms.CheckboxInput(attrs={
#                 "class": "form-check-input"
#             }),

#             "is_featured": forms.CheckboxInput(attrs={
#                 "class": "form-check-input"
#             }),
#         }
    # ✅ FILTER USER DROPDOWN

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

# INPUT = "w-full border px-4 py-3 rounded-xl focus:ring-2 focus:ring-orange-400"


INPUT = "form-control"

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"

        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT}),
            "link": forms.URLInput(attrs={"class": INPUT}),
            "Slot_position": forms.NumberInput(attrs={"class": INPUT}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Location
#         fields = "__all__"
#         widgets = {
#             "name": forms.TextInput(attrs={"class": INPUT}),
#             "slug": forms.TextInput(attrs={"class": INPUT}),
#             "is_active": forms.CheckboxInput(attrs={"class": "w-5 h-5"}),
#         }



# class LocationForm(forms.ModelForm):
#     class Meta:
#         model = Location
#         fields = "__all__"

#         widgets = {
#             "name": forms.TextInput(attrs={
#                 "class": INPUT,
#                 "placeholder":"Enter location name"
#             }),
#         }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"


        widgets = {
            "name": forms.TextInput(attrs={
                "class": INPUT,
                "placeholder": "Enter location name"
            }),
             "slug": forms.TextInput(attrs={
                "class": INPUT,
                "placeholder": "Enter slug (example: gachibowli)"
            }),

             "meta_title": forms.TextInput(attrs={
                "class": INPUT,
                "placeholder": "SEO title "
            }),

            "meta_description": forms.Textarea(attrs={
                "class": INPUT,
                "rows": 3,
                "placeholder": "SEO description"
            }),

            "meta_keywords": forms.TextInput(attrs={
                "class": INPUT,
                "placeholder": "SEO keywords"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }



class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT}),
            "icon_class": forms.TextInput(attrs={
                "class": INPUT,
                "placeholder":"Example: fa-solid fa-wifi"
            }),
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

BOOTSTRAP_INPUT = "form-control"
BOOTSTRAP_TEXTAREA = "form-control"
BOOTSTRAP_FILE = "form-control"
BOOTSTRAP_SELECT = "form-select"
BOOTSTRAP_CHECKBOX = "form-check-input"


class ChooseServiceForm(forms.ModelForm):
    class Meta:
        model = Choos_Services
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Service title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Service description"
            }),
            "icon": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "fa-solid fa-star"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "Slot_position": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }


# class FacilityForm(forms.ModelForm):
#     class Meta:
#         model = Facilities
#         fields = "__all__"
#         widgets = {
#             "name": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
#             "is_active": forms.CheckboxInput(attrs={"class": BOOTSTRAP_CHECKBOX}),
#         }

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facilities
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Facility name"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

# class OurFacilityForm(forms.ModelForm):
#     class Meta:
#         model = OurFacility
#         fields = "__all__"
#         widgets = {
#             "main_title": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
#             "description": forms.Textarea(attrs={"class": BOOTSTRAP_TEXTAREA, "rows": 4}),
#             "image": forms.ClearableFileInput(attrs={"class": BOOTSTRAP_FILE}),
#             "facilities": forms.CheckboxSelectMultiple(
#                 attrs={"class": "form-check-input me-2"}
#             ),
#             "is_active": forms.CheckboxInput(attrs={"class": BOOTSTRAP_CHECKBOX}),
#         }
class OurFacilityForm(forms.ModelForm):
    class Meta:
        model = OurFacility
        fields = "__all__"
        widgets = {
            "main_title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),

            # 🔥 IMPORTANT
            "facilities": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),

            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class WhoWeAreForm(forms.ModelForm):
    class Meta:
        model = WhoWeAre
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "description": forms.Textarea(attrs={"class": BOOTSTRAP_TEXTAREA, "rows": 4}),
            "icon": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "image": forms.ClearableFileInput(attrs={"class": BOOTSTRAP_FILE}),
            "Slot_position": forms.NumberInput(attrs={"class": BOOTSTRAP_INPUT}),
            "is_active": forms.CheckboxInput(attrs={"class": BOOTSTRAP_CHECKBOX}),
        }

class AboutSectionForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = "__all__"
        widgets = {
            "title_tag": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "main_title": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control description-box w-100  ",
                      "style": "width:100%; max-width:100%;",
                    "placeholder": "Write full about description here...",
                    "rows": 10,
                }
            ),

            "image": forms.ClearableFileInput(attrs={"class": BOOTSTRAP_FILE}),
            "video": forms.ClearableFileInput(attrs={"class": BOOTSTRAP_FILE}),
            "is_active": forms.CheckboxInput(attrs={"class": BOOTSTRAP_CHECKBOX}),
        }


class AboutFeatureForm(forms.ModelForm):
    class Meta:
        model = AboutFeature
        fields = "__all__"
        widgets = {
            "about": forms.Select(attrs={"class": BOOTSTRAP_SELECT}),
            "icon": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "title": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "is_active": forms.CheckboxInput(attrs={"class": BOOTSTRAP_CHECKBOX}),
        }


class AboutWhoWeAreForm(forms.ModelForm):
    class Meta:
        model = AboutWhoWeAre
        fields = "__all__"
        widgets = {
            "small_title": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "main_title": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "mission_title": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "mission_description": forms.Textarea(attrs={"class": BOOTSTRAP_TEXTAREA, "rows": 4}),
            "difference_title": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "difference_description": forms.Textarea(attrs={"class": BOOTSTRAP_TEXTAREA, "rows": 4}),
            "image": forms.ClearableFileInput(attrs={"class": BOOTSTRAP_FILE}),
            "button_text": forms.TextInput(attrs={"class": BOOTSTRAP_INPUT}),
            "is_active": forms.CheckboxInput(attrs={"class": BOOTSTRAP_CHECKBOX}),
        }





# coupon

from django import forms
from coupon.models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = "__all__"
        widgets = {
            "farmhouse": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Coupon title"
            }),
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "EXAMPLE10"
            }),
            "discount_type": forms.Select(attrs={
                "class": "form-select"
            }),
            "discount_value": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "min_booking_amount": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "max_discount_amount": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "end_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "usage_limit": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }



# user


from django import forms
from user.models import User
from django import forms
from user.models import User



# from django import forms
# from .models import User

class AdminUserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Leave blank to keep current password"
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone",
            "password",
            "is_staff",
            "farmhouse_user",
            "note",
            'assignedpermission',
            "is_active",
            "farmhouse_limit",
        ]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "farmhouse_user": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "assignedpermission": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
                   # ✅ FIXED NOTE FIELD
            "note": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter admin notes"
            }),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "farmhouse_limit": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Maximum farmhouses allowed"
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        # ✅ Update password only if entered
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)

        # ✅ If farmhouse owner → auto enable staff
        if self.cleaned_data.get("farmhouse_user"):
            user.is_staff = True

        if commit:
            user.save()

        return user
    
    


from contact.models import ContactInfo

BOOTSTRAP = "form-control"

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = "__all__"

        widgets = {
            "phone": forms.TextInput(attrs={"class": BOOTSTRAP}),
            "email_1": forms.EmailInput(attrs={"class": BOOTSTRAP}),
            "email_2": forms.EmailInput(attrs={"class": BOOTSTRAP}),
            "opening_time": forms.TextInput(attrs={
                "class": BOOTSTRAP,
                "placeholder": "8:00AM - 10:00PM, Sunday - Saturday"
            }),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }





from django import forms
from booking.models import Booking


class AdminBookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        exclude = [
            "booking_id",
            "transaction_id",
            "payment_id",
            "confirmation_email_sent_at",
            "cancelled_at",
            "created_at",
            "sub_total",
            "tax_price",
            "disc_price",
            "total_amount",
            "remaining_amount",
        ]

        widgets = {
            # ⭐ NO type="date"
            "check_in": forms.TextInput(),
            "check_out": forms.TextInput(),
        }

    ###################################
    # AUTO APPLY BOOTSTRAP
    ###################################
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"

            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"

            else:
                field.widget.attrs["class"] = "form-control"

        ##################################################
        # ⭐ MAKE DATE FIELDS READONLY (BEST PRACTICE)
        ##################################################

        self.fields["check_in"].widget.attrs.update({
            "readonly": "readonly",
            "placeholder": "Select check-in"
        })

        self.fields["check_out"].widget.attrs.update({
            "readonly": "readonly",
            "placeholder": "Select check-out"
        })



from django import forms
from booking.models import BlockedDate





from django import forms
from booking.models import BlockedDate
from booking.models import Booking
from datetime import date
from django import forms
from datetime import date
from django.core.exceptions import ValidationError
from booking.models import BlockedDate, Booking

from datetime import date, timedelta
from django.core.exceptions import ValidationError


from django import forms
from django.core.exceptions import ValidationError
from datetime import date
# from .models import BlockedDate, Booking


class BlockedDateForm(forms.ModelForm):

    class Meta:
        model = BlockedDate
        fields = "__all__"
        widgets = {
            "farmhouse": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "end_date": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "reason": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        farmhouse = cleaned_data.get("farmhouse")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if not farmhouse or not start_date or not end_date:
            return cleaned_data

        if end_date <= start_date:
            raise ValidationError("End date must be greater than start date.")

        if start_date < date.today():
            raise ValidationError("You cannot block past dates.")

        ##########################################
        # BLOCKED OVERLAP CHECK
        ##########################################
        blocked_qs = BlockedDate.objects.filter(farmhouse=farmhouse)

        if self.instance.pk:
            blocked_qs = blocked_qs.exclude(pk=self.instance.pk)

        for block in blocked_qs:
            overlap = start_date < block.end_date and end_date > block.start_date

            if overlap:
                raise ValidationError(
                    f"❌ You selected {start_date} → {end_date} "
                    f"but it overlaps with existing block "
                    f"{block.start_date} → {block.end_date}"
                )

        ##########################################
        # BOOKING OVERLAP CHECK
        ##########################################
        booking_qs = Booking.objects.filter(
            farmhouse=farmhouse,
            status__in=["pending", "confirmed"]
        )

        for booking in booking_qs:
            overlap = start_date < booking.check_out and end_date > booking.check_in

            if overlap:
                raise ValidationError(
                    f"❌ Conflicts with booking "
                    f"{booking.check_in} → {booking.check_out}"
                )

        return cleaned_data



from django import forms
from blogs.models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"



# locations




# class LocationForm(forms.ModelForm):

#     class Meta:
#         model = Location
#         fields = ['name', 'is_active']

#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter Location Name'
#             }),
#             'is_active': forms.CheckboxInput(attrs={
#                 'class': 'form-check-input'
#             }),
#         }




# forms.py


class FacilityForm(forms.ModelForm):
    class Meta:
        model = FarmhouseFacilities
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }





class CancelReasonForm(forms.ModelForm):
    class Meta:
        model = CancelReason
        fields = ["reason", "is_active"]
        widgets = {
            "reason": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        
        


class ThingstocarryForm(forms.ModelForm):
    class Meta:
        model = Thingstocarry
        fields = ["name", "active", "slot_position"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "slot_position": forms.NumberInput(attrs={"class": "form-control"}),
        }
        
        

class PropertyrulesForm(forms.ModelForm):
    class Meta:
        model = Propertyrules
        fields = ["name", "active", "slot_position"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "slot_position": forms.NumberInput(attrs={"class": "form-control"}),
        }
        
        
        
# class PageSEOForm(forms.ModelForm):
#     class Meta:
#         model = PageSEO
#         fields = "__all__"


class PageSEOForm(forms.ModelForm):
    class Meta:
        model = PageSEO
        fields = "__all__"

        widgets = {
            "page": forms.Select(attrs={
                "class": "form-select"
            }),

            "meta_title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter SEO title"
            }),

            "meta_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Enter meta description (150-160 characters)"
            }),

            "meta_keywords": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "farmhouse, resort, weekend stay"
            }),
        }
        
        



class HomePopupForm(forms.ModelForm):

    class Meta:
        model = HomePopup
        fields = ["image", "farmhouse", "location","is_active" ]
        
        
        
        
# forms.py
from django import forms
from wallet.models import Wallet


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["user", "balance", "wallet_start_date", "wallet_end_date"]

        widgets = {
            "user": forms.Select(attrs={"class": "form-control"}),
            "balance": forms.NumberInput(attrs={"class": "form-control"}),

            "wallet_start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),

            "wallet_end_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
        }