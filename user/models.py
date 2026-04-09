from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    assignedpermission = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    farmhouse_user = models.BooleanField(default=False)
    farmhouse_limit = models.PositiveIntegerField(
        default=10, null=True ,blank=True,
        help_text="Maximum farmhouses allowed for farmhouse owners"
    )
    image = models.ImageField(
        upload_to="users/profile/",
        null=True,
        blank=True,
        default="users/profile/default.png"
    )
    
    note = models.TextField(
    blank=True,
    null=True,
    help_text="Add any notes about this user"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    def __str__(self):
        return self.username


