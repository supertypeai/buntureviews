from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username", "email", "is_staff", "is_active")
