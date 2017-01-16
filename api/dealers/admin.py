from django.contrib import admin

from .models import Dealer, DealerScraper, DealerScraperReport


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


class DealerScraperAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "class_name",
                "dealer",
                "is_active",
            )
        }),
        ("Meta", {
            "classes": ("grp-collapse",),
            "fields": ("created", "id", "modified",)
        })
    )
    list_display = (
        "id",
        "class_name",
        "dealer",
        "created",
        "modified",
    )
    list_filter = ("dealer",)
    readonly_fields = ("created", "id", "modified",)
    search_fields = ("class_name",)


class DealerScraperReportAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "drivers_created",
                "driver_product_listings_created",
                "driver_product_listings_updated",
                "errors",
                "scraper",
            )
        }),
        ("Meta", {
            "classes": ("grp-collapse",),
            "fields": ("created", "id",)
        })
    )
    list_display = (
        "id",
        "scraper",
        "drivers_created",
        "driver_product_listings_created",
        "driver_product_listings_updated",
        "errors",
        "created",
    )
    list_filter = ()
    readonly_fields = ("created", "id",)
    search_fields = ()


admin.site.register(Dealer, DealerAdmin)
admin.site.register(DealerScraper, DealerScraperAdmin)
admin.site.register(DealerScraperReport, DealerScraperReportAdmin)
