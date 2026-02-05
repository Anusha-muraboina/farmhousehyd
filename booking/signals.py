from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Farmhouse, FarmhousePricing


@receiver(post_save, sender=Farmhouse)
def create_pricing(sender, instance, created, **kwargs):
    if created:
        FarmhousePricing.objects.create(
            farmhouse=instance,
            normal_day_price=0,
            weekend_price=0,
            extra_guest_price=0
        )
