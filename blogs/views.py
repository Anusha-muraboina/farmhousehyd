from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Blog, BlogCategory, BlogTag, BlogComment
from django.contrib import messages

from django.shortcuts import render
from django.db.models import Q, Count
from .models import Blog, BlogCategory, BlogTag

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from cms.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from django.db.models import Count, Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Blog, BlogCategory, BlogTag
from .serializers import (
    BlogListSerializer,
    BlogCategorySerializer,
    BlogTagSerializer,
    BlogDetailSerializer
)

class BlogListAPIView(ListAPIView):
    serializer_class = BlogListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True)

        search = self.request.GET.get("search")
        category = self.request.GET.get("category")
        tag = self.request.GET.get("tag")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(content__icontains=search)
            )

        if category:
            queryset = queryset.filter(category__slug=category)

        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset

    def get_serializer_context(self):
        return {"request": self.request}








# class BlogDetailAPIView(RetrieveAPIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [AllowAny]
#     queryset = Blog.objects.filter(is_published=True)
#     serializer_class = BlogListSerializer
#     lookup_field = "slug"

#     def get_serializer_context(self):
#         return {"request": self.request}

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.views += 1
#         instance.save(update_fields=["views"])
#         return super().retrieve(request, *args, **kwargs)


class BlogDetailAPIView(RetrieveAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogDetailSerializer
    lookup_field = "slug"

    def get_serializer_context(self):
        return {"request": self.request}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=["views"])
        return super().retrieve(request, *args, **kwargs)


class BlogCategoryAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    queryset = BlogCategory.objects.filter(is_active=True).annotate(
        blog_count=Count("blogs")
    )
    serializer_class = BlogCategorySerializer


class BlogTagAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer



class RecentBlogsAPIView(ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = BlogListSerializer

    def get_queryset(self):
        return Blog.objects.filter(
            is_published=True
        ).order_by("-published_at")[:5]

    def get_serializer_context(self):
        return {"request": self.request}



def blog_list(request):
    return render(request, "blog_listing.html")


def blog_detail(request, slug):
    return render(request, "blog_detailpage.html", {"slug": slug})



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AddCommentAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug, is_published=True)

        name = request.data.get("name")
        email = request.data.get("email")
        comment = request.data.get("comment")

        if not name or not email or not comment:
            return Response(
                {"error": "All fields required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        BlogComment.objects.create(
            blog=blog,
            name=name,
            email=email,
            comment=comment
        )

        return Response({"success": "Comment added"})








# def blog_list(request):
#     blogs = Blog.objects.filter(is_published=True)

#     category_slug = request.GET.get('category')
#     tag_slug = request.GET.get('tag')
#     search_query = request.GET.get('search')

#     # Filter by category
#     if category_slug:
#         blogs = blogs.filter(category__slug=category_slug)

#     # Filter by tag
#     if tag_slug:
#         blogs = blogs.filter(tags__slug=tag_slug)

#     # Search
#     if search_query:
#         blogs = blogs.filter(
#             Q(title__icontains=search_query) |
#             Q(content__icontains=search_query) |
#             Q(short_description__icontains=search_query)
#         )

#     categories = BlogCategory.objects.filter(is_active=True).annotate(
#         blog_count=Count('blogs')
#     )
#     tags = BlogTag.objects.all()
#     latest_blogs = Blog.objects.filter(is_published=True).order_by('-published_at')[:5]

#     context = {
#         'blogs': blogs,
#         'categories': categories,
#         'tags': tags,
#         'latest_blogs': latest_blogs,
#         'selected_category': category_slug,
#         'selected_tag': tag_slug,
#         'search_query': search_query,
#     }

#     return render(request, 'blog_listing.html', context)

# def blog_detail(request, slug):
#     blog = get_object_or_404(Blog, slug=slug, is_published=True)

#     # 🔥 Increase view count
#     blog.views += 1
#     blog.save(update_fields=["views"])

#     # 💬 Handle comments
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         comment = request.POST.get("comment")

#         if name and email and comment:
#             BlogComment.objects.create(
#                 blog=blog,
#                 name=name,
#                 email=email,
#                 comment=comment
#             )
#             messages.success(request, "Comment submitted for approval.")
#             return redirect("blog_detail", slug=blog.slug)

#     categories = BlogCategory.objects.filter(
#         is_active=True
#     ).annotate(blog_count=Count("blogs"))

#     tags = BlogTag.objects.all()

#     related_blogs = Blog.objects.filter(
#         category=blog.category,
#         is_published=True
#     ).exclude(id=blog.id)[:3]

#     comments = blog.comments.filter(is_active=True)

#     context = {
#         "blog": blog,
#         "categories": categories,
#         "tags": tags,
#         "related_blogs": related_blogs,
#         "comments": comments,
#     }

#     return render(request, "blog_detailpage.html", context)
















# def blog_detail(request, slug):
#     """Detail page for a blog post"""
#     blog = get_object_or_404(Blog, slug=slug, is_published=True)
    
#     # Increase view count
#     blog.views += 1
#     blog.save()
    
#     # Handling comments
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         comment_text = request.POST.get('comment')
        
#         BlogComment.objects.create(
#             blog=blog,
#             name=name,
#             email=email,
#             comment=comment_text
#         )
#         messages.success(request, "Your comment has been submitted and is awaiting approval.")
#         return redirect('blog_detail', slug=blog.slug)
    
#     categories = BlogCategory.objects.filter(is_active=True).annotate(blog_count=Count('blogs'))
#     tags = BlogTag.objects.all()
#     related_blogs = Blog.objects.filter(category=blog.category, is_published=True).exclude(id=blog.id)[:3]
    
#     context = {
#         'blog': blog,
#         'categories': categories,
#         'tags': tags,
#         'related_blogs': related_blogs,
#         'comments': blog.comments.filter(is_active=True).order_by('-created_at')
#     }
#     return render(request, 'blog_detailpage.html', context)
