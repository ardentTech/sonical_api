from django.contrib import admin

from .models import Driver, DriverGroup


class DriverAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Specs", {
            "fields": (
                "dc_resistance",
                "electromagnetic_q",
                "manufacturer",
                "mechanical_q",
                "model",
                "nominal_diameter",
                "rms_power",
                "max_power",
                "nominal_impedance",
                "sensitivity",
                "voice_coil_inductance",
            )
        }),
        ("Thiele-Small", {
            "fields": ("resonant_frequency",)
        }),
        ("Other", {
            "fields": ("in_production",)
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
        "resonant_frequency",
        "sensitivity",
        "rms_power",
        "max_power",
        "created",
        "modified",
    )
    list_filter = ("in_production", "manufacturer",)
    readonly_fields = ("created", "id", "modified",)
    search_fields = ("model",)


class DriverGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "drivers",
                "name"
            )
        }),
        ("Meta", {
            "classes": ("grp-collapse",),
            "fields": ("created", "id", "modified",)
        })
    )
    list_display = ("id", "name", "created", "modified",)
    readonly_fields = ("created", "id", "modified",)
    search_fields = ("name",)


admin.site.register(Driver, DriverAdmin)
admin.site.register(DriverGroup, DriverGroupAdmin)
