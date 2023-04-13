from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_staff",
        "date_joined",
    )
