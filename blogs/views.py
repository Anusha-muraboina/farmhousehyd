from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Blog, BlogCategory, BlogTag, BlogComment
from django.contrib import messages

from django.shortcuts import render
from django.db.models import Q, Count
from .models import Blog, BlogCategory, BlogTag

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True)

    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    search_query = request.GET.get('search')

    # Filter by category
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)

    # Filter by tag
    if tag_slug:
        blogs = blogs.filter(tags__slug=tag_slug)

    # Search
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )

    categories = BlogCategory.objects.filter(is_active=True).annotate(
        blog_count=Count('blogs')
    )
    tags = BlogTag.objects.all()
    latest_blogs = Blog.objects.filter(is_published=True).order_by('-published_at')[:5]

    context = {
        'blogs': blogs,
        'categories': categories,
        'tags': tags,
        'latest_blogs': latest_blogs,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
        'search_query': search_query,
    }

    return render(request, 'blog_listing.html', context)

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)

    # 🔥 Increase view count
    blog.views += 1
    blog.save(update_fields=["views"])

    # 💬 Handle comments
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        comment = request.POST.get("comment")

        if name and email and comment:
            BlogComment.objects.create(
                blog=blog,
                name=name,
                email=email,
                comment=comment
            )
            messages.success(request, "Comment submitted for approval.")
            return redirect("blog_detail", slug=blog.slug)

    categories = BlogCategory.objects.filter(
        is_active=True
    ).annotate(blog_count=Count("blogs"))

    tags = BlogTag.objects.all()

    related_blogs = Blog.objects.filter(
        category=blog.category,
        is_published=True
    ).exclude(id=blog.id)[:3]

    comments = blog.comments.filter(is_active=True)

    context = {
        "blog": blog,
        "categories": categories,
        "tags": tags,
        "related_blogs": related_blogs,
        "comments": comments,
    }

    return render(request, "blog_detailpage.html", context)

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
