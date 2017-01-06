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

    class Meta:
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
    scraper = models.ForeignKey(
        "scrapers.Scraper",
        verbose_name=_("scraper"))

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "Report for {0} Scraper".format(self.scraper.name)
