
from django import forms
from farmhouse.models import *


from django import forms
from booking.models import BlockedDate
from django import forms
from farmhouse.models import Farmhouse

class FarmhouseForm(forms.ModelForm):

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

            "guest_count": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "amenities": forms.SelectMultiple(attrs={
                "class": "form-select",
                "style": "height:120px"
            }),

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
        }


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




class BlockedDateForm(forms.ModelForm):

    class Meta:
        model = BlockedDate
        fields = "__all__"

        widgets = {
            "start_date": forms.TextInput(attrs={"class":"form-control"}),
            "end_date": forms.TextInput(attrs={"class":"form-control"}),
            "reason": forms.TextInput(attrs={"class":"form-control"}),
        }