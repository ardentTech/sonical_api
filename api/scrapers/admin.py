from django.contrib import admin

from .models import Scraper, ScraperReport


admin.site.register(Scraper)
admin.site.register(ScraperReport)
