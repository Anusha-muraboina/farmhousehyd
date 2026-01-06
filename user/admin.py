from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'phone', 'assignedpermission', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'assignedpermission')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'assignedpermission')}),
    )

admin.site.register(User, CustomUserAdmin)
