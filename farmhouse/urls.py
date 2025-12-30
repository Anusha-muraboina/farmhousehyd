# urls.py
from django.urls import path
from .views import blog_page

urlpatterns = [
    path('blogs/', blog_page, name='blogs'),
]
