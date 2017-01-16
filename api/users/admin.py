from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class SonicalUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "email",
                "is_active",
                "is_staff",
                "is_superuser",
                "last_login",
            )
        }),
        ("Meta", {
            "classes": ("grp-collapse",),
            "fields": ("created", "id", "modified",)
        })
    )
    list_display = (
        "id",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "created",
        "modified",
    )
    list_filter = ("is_active", "is_staff", "is_superuser",)
    ordering = ("email",)
    readonly_fields = ("created", "id", "last_login", "modified",)
    search_fields = ("email",)


admin.site.register(User, SonicalUserAdmin)
