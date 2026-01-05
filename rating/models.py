from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


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

#     rating = models.PositiveIntegerField()

#     review = models.TextField(
#         blank=True,
#         null=True,
#         help_text="Optional review message"
#     )

#     is_active = models.BooleanField(default=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.rating}★"



