from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable
from utils.validators import validate_file_path


class Scraper(Creatable, Modifiable):

    name = models.CharField(
        _("name"),
        max_length=128)
    file_path = models.CharField(
        _("file path"),
        max_length=128,
        validators=[validate_file_path])
    is_active = models.BooleanField(
        _("is active"),
        default=False)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class ScraperReport(Creatable):

    attempted = models.PositiveIntegerField(
        _("attempted"),
        default=0)
    processed = models.PositiveIntegerField(
        _("processed"),
        default=0)

    class Meta:
        abstract = True
        ordering = ["-id"]

    def __str__(self):
        return "Report for {0} Scraper".format(self.scraper.name)
