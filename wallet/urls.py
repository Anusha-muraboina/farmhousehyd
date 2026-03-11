# urls.py
from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path("wallet/", views.wallet, name="wallet"),
     path("balance/", views.wallet_balance),
]

