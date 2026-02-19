from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blogs.models import Blog

class BlogListSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return ["blog_list"]

    def location(self, item):
        return reverse(item)


class BlogDetailSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Blog.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, "updated_at") else obj.published_at
