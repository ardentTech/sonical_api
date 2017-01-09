import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable


class ProductListing(Creatable, Modifiable):

    dealer = models.ForeignKey(
        "dealers.Dealer",
        verbose_name=_("dealer"))
    path = models.CharField(
        _("path"),
        max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def listing_url(self):
        return "".join(self.dealer.website, self.path)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if len(self.path) and self.path[0] != os.sep:
            self.path = os.sep + self.path
        super(ProductListing, self).save(*args, **kwargs)
