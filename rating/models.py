from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# from product.models import *
# from django.utils.html import mark_safe
# from user.models import User
# class Rating(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="ratings"
#     )

#     farmhouse = models.ForeignKey(
#         'Farmhouse',  # change if model name differs
#         on_delete=models.CASCADE,
#         related_name="ratings"
#     )

#     rating = models.IntegerField()

#     review = models.TextField(
#         blank=True,
#         null=True,
#         help_text="Optional review message"
#     )
    #   anonymous = models.BooleanField(default=False)
#     active = models.BooleanField(default=True)

#     review_date = models.DateTimeField(default=timezone.now)
    # def display_stars(self):
    #     full_stars = int(self.stars)
    #     half_star = self.stars - full_stars
    #     empty_stars = 5 - full_stars - (1 if half_star else 0)

    #     full_star_icon = '<i class="fas fa-star"></i>'
    #     half_star_icon = '<i class="fas fa-star-half-alt"></i>'
    #     empty_star_icon = '<i class="far fa-star"></i>'

    #     stars_html = (full_star_icon * full_stars +
    #                   (half_star_icon if half_star else '') +
    #                   empty_star_icon * empty_stars)

    #     return mark_safe(stars_html)
#     def __str__(self):
#         return f"{self.user.username} - {self.rating}★"



# class RatingImage(models.Model):
#     rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
#     photo = models.ImageField(upload_to='rating_images/')
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Image for rating by {self.rating.user.username}"