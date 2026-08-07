from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from farmhouse.models import Farmhouse ,Location
from blogs.models import Blog


####################################################
# STATIC PAGES
####################################################
class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
            "home",
            "about",
            "contact",
            "farmhouses",
            "privacy_policy",
            "terms_conditions",
            "refund_policy",
            "bloglisting",
        ]

    def location(self, item):
        return reverse(item)


####################################################
# FARMHOUSE DETAIL PAGES
####################################################
class FarmhouseSitemap(Sitemap):

    def items(self):
        return Farmhouse.objects.filter(is_active=True, is_deleted=False)

    def location(self, obj):
        return reverse(
            "farmhouse_detail",
            args=[obj.slug, obj.location.slug] ,
            
            
        )
        


# class FarmhouseLocationSitemap(Sitemap):
#     def items(self):
#         return Location.objects.filter(is_active=True)

#     def location(self, obj):
#         return reverse(
#             "farmhouses-location",
#             kwargs={
#                 "location": obj.meta_title.replace(" ", "_")
#             }
#         )
class FarmhouseLocationSitemap(Sitemap):

    def items(self):
        return Location.objects.filter(
            is_active=True
        ).exclude(meta_title="")

    def location(self, obj):
        title = (obj.meta_title or "").strip()

        return reverse(
            "farmhouses-location",
            kwargs={
                "location": title.replace(" ", "_")
            }
        )
####################################################
# BLOG DETAIL PAGES
####################################################
class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Blog.objects.filter(is_published=True)

    def lastmod(self, obj):
        return getattr(obj, "updated_at", obj.published_at)

    def location(self, obj):
        return reverse("blog_detail", args=[obj.slug])