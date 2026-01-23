from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    assignedpermission = models.BooleanField(default=False)
    phone = models.CharField(max_length=15)
    farmhouse_user = models.BooleanField(default=False)
    def __str__(self):
        return self.username


