
from django import forms
from farmhouse.models import *


from django import forms
from booking.models import BlockedDate ,Booking
from django import forms
from farmhouse.models import Farmhouse 
from booking.models import FarmhousePaymentPolicy
import json
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
class FarmhouseImageForm(forms.ModelForm):
    class Meta:
        model = FarmhouseImage
        fields = ["image", "is_primary"]

        widgets = {
            "image": forms.FileInput(attrs={
                "class": "form-control"
            }),
            "is_primary": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
        
class FarmhouseForm(forms.ModelForm):
    weekend_days = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "[5,6] (Sat, Sun)"
        }),
        help_text="Enter like [5,6] for Sat & Sun"
    )
    class Meta:
        model = Farmhouse
        exclude = ("user", "slug", "created_at")

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control ",
                "placeholder": "Enter farmhouse title"
            }),
            "location": forms.Select(attrs={
                "class": "form-select "
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Full address"
            }),
            "distance_km": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "bedrooms": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "halls": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "ac_bedrooms": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            
            
            
           "map_embed": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
           

            # "guest_count": forms.NumberInput(attrs={
            #     "class": "form-control"
            # }),
            # "amenities": forms.SelectMultiple(attrs={
            #     "class": "form-select",
            #     "style": "height:120px"
            # }),
            "amenities": forms.CheckboxSelectMultiple(),
            "thingstocarry": forms.CheckboxSelectMultiple(),
            "properyrules": forms.CheckboxSelectMultiple(),
            "facilities": forms.CheckboxSelectMultiple(),
            
            "guest_count": forms.NumberInput(attrs={"class": "form-control"}),
            "extra_guest_count": forms.NumberInput(attrs={"class": "form-control"}),
            "commission_percentage": forms.NumberInput(attrs={"class": "form-control"}),
            
            "meta_title": forms.TextInput(attrs={"class": "form-control"}),
            "meta_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "meta_keywords": forms.TextInput(attrs={"class": "form-control"}),
            
            "short_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 10
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 15
            }),
            "price_per_day": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "free_cancellation": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_featured": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            
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
            
        }
    def clean_weekend_days(self):
        data = self.cleaned_data.get("weekend_days")

        if not data:
            return [5, 6]  # default

        try:
            parsed = json.loads(data)

            if not isinstance(parsed, list):
                raise forms.ValidationError("Must be a list like [5,6]")

            return [int(x) for x in parsed]

        except Exception:
            raise forms.ValidationError("Invalid format. Example: [5,6]")
        
        

from django import forms
from coupon.models import Coupon


class OwnerCouponForm(forms.ModelForm):

    class Meta:
        model = Coupon

        exclude = (
            "farmhouse",
            "created_at",
        )

        widgets = {

            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),

            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }




# class BlockedDateForm(forms.ModelForm):

#     class Meta:
#         model = BlockedDate
#         fields = "__all__"

#         widgets = {
#             "start_date": forms.TextInput(attrs={"class":"form-control"}),
#             "end_date": forms.TextInput(attrs={"class":"form-control"}),
#             "reason": forms.TextInput(attrs={"class":"form-control"}),
#         }

from django import forms
from booking.models import BlockedDate

class BlockedDateForm(forms.ModelForm):

    class Meta:
        model = BlockedDate
        fields = "__all__"

        widgets = {
            "farmhouse": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.TextInput(attrs={"class":"form-control"}),
            "end_date": forms.TextInput(attrs={"class":"form-control"}),
            "reason": forms.TextInput(attrs={"class":"form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["farmhouse"].queryset = user.farmhouses.all()



# forms.py

class FarmhousePaymentPolicyForm(forms.ModelForm):
    class Meta:
        model = FarmhousePaymentPolicy
        fields = "__all__"


# class ownerBookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking   # 🔥 THIS WAS MISSING
#         fields = "__all__"
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop("user", None)
#         super().__init__(*args, **kwargs)

#         if user:
#             # 🔥 ONLY THIS OWNER'S FARMHOUSES
#             self.fields["farmhouse"].queryset = Farmhouse.objects.filter(user=user)
#         # if user and not user.is_superuser:
#         #     self.fields["farmhouse"].queryset = Farmhouse.objects.filter(user=user)
        
from django.contrib.auth import get_user_model   
User = get_user_model()

class ownerBookingForm(forms.ModelForm):

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
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # 🔥 FILTER FARMHOUSES HERE
        if user:
            self.fields["farmhouse"].queryset = Farmhouse.objects.filter(user=user)

                       # 🔥 Only owner's coupons
            # 🔥 Only coupons of owner's farmhouses
            self.fields["coupon_applied"].queryset = Coupon.objects.filter(
                farmhouse__user=user,
                is_active=True
            )
            
                ###################################
            # ✅ FILTER ONLY NORMAL USERS 
            ###################################
        if "user" in self.fields:
            self.fields["user"].queryset = User.objects.filter(
                is_staff=False,
            is_superuser=False
            )

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
        self.fields["special_requests"].widget = forms.Textarea(attrs={
            "rows": 3,
            "class": "form-control",
            "placeholder": "Enter special requests"
        })





from farmhouse.models import FarmhouseOfferPricing

class FarmhouseOfferForm(forms.ModelForm):
    class Meta:
        model = FarmhouseOfferPricing
        fields = ["farmhouse", "title", "start_date", "end_date", "price"]

        widgets = {
            "farmhouse": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter offer title"
            }),
            "start_date": forms.HiddenInput(),   # 👈 hidden
            "end_date": forms.HiddenInput(),     # 👈 hidden
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter price"
            }),
        }
        
        

from django import forms

from rating.models import Rating


class RatingForm(forms.ModelForm):

    class Meta:

        model = Rating

        exclude = ["created_at"]

        widgets = {

            "user": forms.Select(
                attrs={
                    "class": "form-select custom-input"
                }
            ),

            "farmhouse": forms.Select(
                attrs={
                    "class": "form-select custom-input"
                }
            ),

            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Enter rating",
                    "step": "0.1",
                    "min": "1",
                    "max": "5"
                }
            ),

            "review": forms.Textarea(
                attrs={
                    "class": "form-control custom-input",
                    "placeholder": "Write review...",
                    "rows": 5
                }
            ),

            "anonymous": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

        }