from django.db import models
from django.utils.translation import ugettext_lazy as _


class Manufacturer(models.Model):

    name = models.CharField(
        _("Name"),
        max_length=128)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Material(models.Model):

    name = models.CharField(
        _("Name"),
        max_length=128)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
