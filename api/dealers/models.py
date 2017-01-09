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
