from django.db import models
from django.utils.translation import ugettext_lazy as _

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


class ProductListing(Creatable, Modifiable):

    dealer = models.ForeignKey(
        "products.Dealer",
        verbose_name=_("dealer"))
    path = models.CharField(
        _("path"),
        max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def listing(self):
        return "".join(self.dealer.website, self.path)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if len(self.path) and self.path[0] != "/":
            self.path = "/" + self.path
        super(Dealer, self).save(*args, **kwargs)
