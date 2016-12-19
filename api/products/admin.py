from django.contrib import admin

from .models import Dealer


class DealerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "name",
                "website",
            )
        }),
        ("Meta", {
            "classes": ("grp-collapse",),
            "fields": ("created", "id", "modified",)
        })
    )
    list_display = (
        "id",
        "name",
        "website",
        "created",
        "modified",
    )
    list_filter = ()
    readonly_fields = ("created", "id", "modified",)
    search_fields = ("model", "website",)


admin.site.register(Dealer, DealerAdmin)