# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    # path('destination/',destination,name= 'destination'),
    # path('farmhouses/', Farmhouses, name = 'farmhouses'),
    # path('farmhouse/', Farmhouse_detail, name='farmhouse_detail'),
    
    path('farmhouses/', Farmhouses, name = 'farmhouses'),
    path('farmhouse/<slug:slug>/<slug:location_slug>/', Farmhouse_detail, name='farmhouse_detail'),
        
    path("api/farmhouses/", FarmhouseListAPI.as_view(), name="api_farmhouses"),
    path("api/farmhouses/<slug:slug>/", FarmhouseDetailAPI.as_view(), name="api_farmhouse_detail"),
    
    # path('login/', Login, name = 'login'),
    # path('register/', Register, name = 'register'),
    
    # path('password-reset/', PasswordResetView, name='passwsord_reset'),
    
    path('bloglisting/', BlogListing,name= 'bloglisting'),
    path('blogdetail/',BlogDetail,name='blogdetail'),
    
    
    # API
    path("api/home/", HomeAPIView.as_view(), name="home-api"),
    path("api/about/", AboutAPIView.as_view(), name="about-api"),
    
    
        # homepage
    # path("", HomeAPIView.as_view(), name="home"),
# 
        # location page
    path("<str:location>/", home_page, name="home-location"),
    path("farmhouses/<str:location>/", Farmhouses, name="farmhouses-location"),
    
    
    
  
]
