from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable


class Manufacturer(Creatable, Modifiable):

    name = models.CharField(
        _("Name"),
        max_length=128)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Material(Creatable, Modifiable):

    name = models.CharField(
        _("Name"),
        max_length=128)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
