from django.urls import path
from .views import *

urlpatterns = [
    path('rating/', rating, name='rating'),
    path("add-review/", AddReviewAPI.as_view()),
    path( "farmhouse-reviews/<slug:slug>/",  farmhouse_reviews,  name="farmhouse_reviews")
]
