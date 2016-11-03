from django.db import models
from django.utils.translation import ugettext_lazy as _


class Creatable(models.Model):

    created = models.DateTimeField(
        _("created"),
        auto_now_add=True)

    class Meta:
        abstract = True


class Modifiable(models.Model):

    modified = models.DateTimeField(
        _("modified"),
        auto_now=True)

    class Meta:
        abstract = True
