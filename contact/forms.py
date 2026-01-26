# from django import forms
# from .models import ContactMessage
# from farmhouse.models import Farmhouse

# class ContactForm(forms.ModelForm):
#     farmhouse = forms.ModelChoiceField(
#         queryset=Farmhouse.objects.filter(is_active=True),
#         empty_label="Select Farmhouse",
#         required=False,
#         widget=forms.Select(attrs={
#             "class": "w-full px-4 py-3 rounded-lg border focus:ring-2 focus:ring-orange-500"
#         })
#     )

#     class Meta:
#         model = ContactMessage
#         fields = ["farmhouse","name", "phone", "email", "message"]

#         widgets = {
#             "name": forms.TextInput(attrs={
#                 "class": "w-full px-4 py-3 rounded-lg border focus:ring-2 focus:ring-green-500",
#                 "placeholder": "Enter your Name"
#             }),
#             "phone": forms.TextInput(attrs={
#                 "class": "w-full px-4 py-3 rounded-lg border focus:ring-2 focus:ring-green-500",
#                 "placeholder": "Phone Number"
#             }),
#             "email": forms.EmailInput(attrs={
#                 "class": "w-full px-4 py-3 rounded-lg border focus:ring-2 focus:ring-green-500",
#                 "placeholder": "Email Address"
#             }),
#             "message": forms.Textarea(attrs={
#                 "rows": 6,
#                 "class": "w-full px-4 py-3 rounded-lg border focus:ring-2 focus:ring-green-500",
#                 "placeholder": "What's on your mind"
#             }),
#         }
