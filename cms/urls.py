from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path("cms/", views.cms, name="cms"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions"),
    path("refund_policy/", views.refund_policy, name="refund_policy"), 
    
    
]
