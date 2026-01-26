# urls.py
from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path("contact/", views.contact, name="contact"),
    
    path("api/contact-info/", ContactInfoAPIView.as_view()),
    path("api/contact-message/", ContactMessageAPIView.as_view()),
    path("api/farmhouses/", FarmhouseListAPIView.as_view()),
]

