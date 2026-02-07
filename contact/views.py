from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# def contact(request):
#     return HttpResponse("This is the Contact Page")


# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings

# from .forms import ContactForm
# from .models import ContactInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import ContactInfo, ContactMessage
from farmhouse.models import Farmhouse
from .serializers import (
    ContactInfoSerializer,
    ContactMessageSerializer,
    FarmhouseSimpleSerializer
)
def contact(request):
    # return HttpResponse("Hello, this is Blog Page")
    return render(request , "contact.html")


# ✅ CONTACT INFO
class ContactInfoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        info = ContactInfo.objects.filter(is_active=True).first()
        serializer = ContactInfoSerializer(info)
        return Response(serializer.data)

class FarmhouseListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        farms = Farmhouse.objects.filter(is_active=True)
        serializer = FarmhouseSimpleSerializer(farms, many=True)
        return Response(serializer.data)

# ✅ FARMHOUSE LIST
class FarmhouseListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        farms = Farmhouse.objects.filter(is_active=True)
        serializer = FarmhouseSimpleSerializer(farms, many=True)
        return Response(serializer.data)


# ✅ CONTACT MESSAGE SUBMIT
class ContactMessageAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "Message sent successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def contact(request):

#     contact_info = ContactInfo.objects.filter(is_active=True).first()

#     if request.method == "POST":
#         form = ContactForm(request.POST)

#         if form.is_valid():
#             contact = form.save()

#             # ================= ADMIN EMAIL =================
#             admin_html = render_to_string(
#                 "emails/contact_admin.html",
#                 {"contact": contact}
#             )

#             admin_email = EmailMultiAlternatives(
#                 subject="New Contact Message",
#                 body="New contact received",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[settings.ADMIN_EMAIL],
#             )
#             admin_email.attach_alternative(admin_html, "text/html")
#             admin_email.send(fail_silently=True)

#             messages.success(request, "Your message has been sent successfully.")
#             return redirect("contact")

#     else:
#         form = ContactForm()

#     return render(request, "contact.html", {
#         "form": form,
#         "contact_info": contact_info
#     })
