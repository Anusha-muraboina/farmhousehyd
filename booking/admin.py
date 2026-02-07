from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Booking)
admin.site.register(Invoice)
admin.site.register(CancelReason)
admin.site.register(OrderCancelComment)
# admin.site.register(BlockedDate)
from django.contrib import admin
from .models import BlockedDate


@admin.register(BlockedDate)
class BlockedDateAdmin(admin.ModelAdmin):

    list_display = (
        "farmhouse",
        
        "start_date",
        "end_date",
        "reason"
    )

    list_filter = ("farmhouse",)

    search_fields = ("farmhouse__title",)

