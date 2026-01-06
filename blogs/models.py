# from django.db import models

# # Create your models here.
# from django.db import models
# from django.utils.text import slugify
# from django.utils import timezone


# class BlogCategory(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)

#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name


# class BlogTag(models.Model):
#     name = models.CharField(max_length=50)
#     slug = models.SlugField(unique=True)

#     def __str__(self):
#         return self.name


# class Blog(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True, blank=True)

#     category = models.ForeignKey(
#         BlogCategory,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='blogs'
#     )

#     tags = models.ManyToManyField(
#         BlogTag,
#         blank=True,
#         related_name='blogs'
#     )

#     image = models.ImageField(upload_to='blogs/')
#     short_description = models.TextField(
#         help_text="Shown in blog listing page"
#     )

#     content = models.TextField(
#         help_text="Full blog content"
#     )

#     views = models.PositiveIntegerField(default=0)
#     read_time = models.PositiveIntegerField(
#         help_text="Read time in minutes (e.g. 3)",
#         default=3
#     )

#     is_published = models.BooleanField(default=True)
#     published_at = models.DateTimeField(default=timezone.now)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-published_at']

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)




# class BlogComment(models.Model):
#     blog = models.ForeignKey(
#         Blog,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )

#     name = models.CharField(max_length=150)
#     email = models.EmailField()
#     comment = models.TextField()

#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.blog.title}"
