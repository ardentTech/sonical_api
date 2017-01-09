from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable


class Scraper(Creatable, Modifiable):

    class_name = models.CharField(
        _("class name"),
        max_length=128)
    is_active = models.BooleanField(
        _("is active"),
        default=True)

    class Meta:
        abstract = True
        ordering = ["class_name"]

    def __str__(self):
        return self.class_name


class ScraperReport(Creatable):

    attempted = models.PositiveIntegerField(
        _("attempted"),
        default=0)
    processed = models.PositiveIntegerField(
        _("processed"),
        default=0)

    class Meta:
        abstract = True
        ordering = ["id"]
