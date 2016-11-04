from django.contrib import admin

from .models import Driver


class DriverAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "diameter",
                "in_production",
                "manufacturer",
                "max_power",
                "model",
                "nominal_impedance",
                "resonant_frequency",
                "rms_power",
                "sensitivity",
            )
        }),
        ("Meta", {
            "classes": ("grp-collapse",),
            "fields": ("created", "id", "modified",)
        })
    )
    list_display = (
        "id",
        "model",
        "manufacturer",
        "nominal_impedance",
        "created",
        "modified",
    )
    list_filter = ("in_production", "manufacturer",)
    readonly_fields = ("created", "id", "modified",)
    search_fields = ("model",)


admin.site.register(Driver, DriverAdmin)
