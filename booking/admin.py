from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Booking)
admin.site.register(Invoice)
admin.site.register(CancelReason)
admin.site.register(OrderCancelComment)
admin.site.register(BlockedDate)
