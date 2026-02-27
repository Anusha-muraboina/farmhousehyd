from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Blog, BlogCategory, BlogTag, BlogComment
from django.contrib import messages



from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from cms.models import *

from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework.generics import ListAPIView, RetrieveAPIView


from rest_framework import status



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



# def blog_list(request):
#     return render(request, "blog_listing.html")



def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)

    # 🔎 Get SEO data for blog listing page
    seo = PageSEO.objects.filter(page="blog").first()  
    # 👉 if you add "blog" choice later, change to page="blog"

    context = {
        "blogs": blogs,

        # ⭐ Dynamic SEO with fallback
        "meta_title": seo.meta_title if seo else "Blog | Vivaan Farmhouse",
        "meta_description": seo.meta_description if seo else "Read the latest tips, travel guides, and updates from Vivaan Farmhouse.",
        "meta_keywords": seo.meta_keywords if seo else "farmhouse blog, travel blog, weekend getaway tips",
    }

    return render(request, "blog_listing.html", context)


# def blog_detail(request, slug):
#     return render(request, "blog_detailpage.html", {"slug": slug})



def blog_detail(request, slug):
    blog = get_object_or_404(
        Blog,
        slug=slug,
        is_published=True
    )

    context = {
        "blog": blog,
        "slug": slug,

        # ⭐ Dynamic SEO with fallback
        "meta_title": blog.meta_title or blog.title,
        "meta_description": blog.meta_description or blog.short_description,
        "meta_keywords": blog.meta_keywords,
    }

    return render(request, "blog_detailpage.html", context)


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