# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('destination/',destination,name= 'destination'),
    path('farmhouses/', Farmhouses, name = 'farmhouses'),
    path('farmhouse/', Farmhouse_detail, name='farmhouse_detail'),
    
    path('login/', Login, name = 'login'),
    path('register/', Register, name = 'register'),
    
    path('password-reset/', PasswordResetView, name='password_reset'),
]
