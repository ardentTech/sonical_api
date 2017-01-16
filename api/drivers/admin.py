from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma

from .models import Driver, DriverGroup, DriverProductListing


class DriverProductListingInline(admin.TabularInline):
    model = DriverProductListing


class DriverAdmin(admin.ModelAdmin):
    inlines = [DriverProductListingInline]
    fieldsets = (
        ("Specs", {
            "fields": (
                "frequency_response",
                "manufacturer",
                "model",
                "nominal_diameter",
                "rms_power",
                "max_power",
                "nominal_impedance",
                "sensitivity",
                "voice_coil_diameter",
                "voice_coil_inductance",
            )
        }),
        ("Thiele-Small", {
            "fields": (
                "bl_product",
                "dc_resistance",
                "diaphragm_mass_including_airload",
                "electromagnetic_q",
                "mechanical_q",
                "resonant_frequency",
            )
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
        "_nominal_impedance",
        "_resonant_frequency",
        "_sensitivity",
        "_rms_power",
        "_max_power",
        "created",
        "modified",
    )
    list_filter = ("in_production", "manufacturer", "nominal_impedance",)
    readonly_fields = ("created", "id", "modified",)
    search_fields = ("model",)

    # @todo use general formatters like the client app
    def _max_power(self, obj):
        return str(obj.max_power) + " W"
    _max_power.short_description = "Max power "
    _max_power.admin_order_field = "max_power"

    def _nominal_impedance(self, obj):
        return str(obj.nominal_impedance) + "Ω"
    _nominal_impedance.short_description = "Nominal Impedance"
    _nominal_impedance.admin_order_field = "nominal_impedance"

    def _resonant_frequency(self, obj):
        return str(obj.resonant_frequency) + " Hz"
    _resonant_frequency.short_description = "Resonant Frequency"
    _resonant_frequency.admin_order_field = "resonant_frequency"

    def _rms_power(self, obj):
        return str(obj.rms_power) + " W"
    _rms_power.short_description = "RMS power "
    _rms_power.admin_order_field = "rms_power"

    def _sensitivity(self, obj):
        return str(obj.sensitivity) + " dB"
    _sensitivity.short_description = "Sensitivity"
    _sensitivity.admin_order_field = "sensitivity"


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


class DriverProductListingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "dealer",
                "driver",
                "path",
                "price",
            )
        }),
        ("Meta", {
            "classes": ("grp-collapse",),
            "fields": ("created", "id", "modified",)
        })
    )
    list_display = (
        "id", "driver", "_manufacturer", "dealer", "_price", "created", "modified",)
    list_filter = ("dealer",)
    readonly_fields = ("created", "id", "modified",)

    def _manufacturer(self, obj):
        return obj.driver.manufacturer.name
    _manufacturer.short_description = "Manufacturer"
#    _manufacturer.admin_order_field = "name"

    def _price(self, obj):
        return "$" + str(intcomma(obj.price))
    _price.short_description = "Price"
    _price.admin_order_field = "price"


admin.site.register(Driver, DriverAdmin)
admin.site.register(DriverGroup, DriverGroupAdmin)
admin.site.register(DriverProductListing, DriverProductListingAdmin)
