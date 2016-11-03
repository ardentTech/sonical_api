from django.contrib import admin

from .models import Manufacturer, Material


admin.site.register(Manufacturer)
admin.site.register(Material)
