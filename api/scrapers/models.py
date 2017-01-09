from os import sep
import pdb

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable
from utils.validators import validate_file_path


class Scraper(Creatable, Modifiable):

    file_path = models.CharField(
        _("file path"),
        max_length=128,
        validators=[validate_file_path])
    is_active = models.BooleanField(
        _("is active"),
        default=True)

    class Meta:
        abstract = True
        ordering = ["id"]

    def run(self):
        parts = self.file_path.split(".")[0].split(sep)
        pdb.set_trace()
#        mod = __import__(".".join(parts[:-1]), fromlist=[parts[-1:]])
#        cls = mod.PartsExpressScraper


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
