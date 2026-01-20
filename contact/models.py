from django.db import models

# Create your models here.

from django.db import models

from farmhouse.models import *
class ContactInfo(models.Model):
    phone = models.CharField(max_length=20)
    email_1 = models.EmailField()
    email_2 = models.EmailField(blank=True, null=True)

    opening_time = models.CharField(
        max_length=100,
        help_text="Example: 8:00AM - 10:00PM, Sunday - Saturday"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.phone


from django.db import models


class ContactMessage(models.Model):
    farmhouse = models.ForeignKey(
        Farmhouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_messages'
    )

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
