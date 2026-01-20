# urls.py
from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path("contact/", views.contact, name="contact"),
]

