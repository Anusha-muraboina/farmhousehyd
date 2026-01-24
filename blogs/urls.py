from django.urls import path
from .views import *

urlpatterns = [
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/<slug:slug>/', blog_detail, name='blog_detail'),
    
    
    path("api/blogs/", BlogListAPIView.as_view()),
    path("api/blogs/<slug:slug>/", BlogDetailAPIView.as_view()),
    path("api/blog-categories/", BlogCategoryAPIView.as_view()),
    path("api/blog-tags/", BlogTagAPIView.as_view()),

    path("api/blogs-recent/", RecentBlogsAPIView.as_view()),
    path("api/blogs/<slug:slug>/comment/", AddCommentAPIView.as_view()),

]
