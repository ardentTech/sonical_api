from django.contrib import admin

from .models import Manufacturer, Material


class ManufacturerAdmin(admin.ModelAdmin):
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
        "created",
        "modified",
    )
    list_filter = ()
    readonly_fields = ("created", "id", "modified",)
    search_fields = ("model",)


class MaterialAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "name",
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
        "created",
        "modified",
    )
    list_filter = ()
    readonly_fields = ("created", "id", "modified",)
    search_fields = ("model",)


admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Material, MaterialAdmin)
