import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from scrapers.models import Scraper, ScraperReport
from utils.models import Creatable, Modifiable


class Dealer(Creatable, Modifiable):

    name = models.CharField(
        _("name"),
        db_index=True,
        max_length=128,
        unique=True)
    website = models.URLField(
        _("website"),
        blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.website.rstrip("/")
        super(Dealer, self).save(*args, **kwargs)


class DealerScraper(Scraper):

    dealer = models.ForeignKey(
        "dealers.Dealer",
        verbose_name=_("dealer"))

    def run(self):
        package = ".".join([os.path.abspath(__file__).split("/")[-2], "scrapers"])
        mod = __import__(package, fromlist=[self.class_name])
        getattr(mod, self.class_name)(self.dealer).run()


class DealerScraperReport(ScraperReport):

    scraper = models.ForeignKey(
        "dealers.DealerScraper",
        verbose_name=_("scraper"))
