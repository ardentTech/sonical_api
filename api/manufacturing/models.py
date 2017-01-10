from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable


class Manufacturer(Creatable, Modifiable):

    # @todo is_active?
    name = models.CharField(
        _("Name"),
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


class Material(Creatable, Modifiable):

    name = models.CharField(
        _("Name"),
        db_index=True,
        max_length=128,
        unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
