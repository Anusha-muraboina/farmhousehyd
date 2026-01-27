from django.urls import path
from .views import *

urlpatterns = [
    path("login/", owner_login, name="owner_login"),
    path("dashboard/", owner_dashboard, name="owner_dashboard"),
    path('farmhouse/',owner_farmhouse ,name = "owner_farmhouse"),
    path("logout/", owner_logout, name="owner_logout"),
]
