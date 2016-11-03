from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable


class Driver(Creatable, Modifiable):

    diameter = models.FloatField(
        _("Diameter (Millimeters)"),
        blank=True,
        null=True)
    manufacturer = models.ForeignKey(
        "manufacturing.Manufacturer")
    max_power = models.IntegerField(
        _("Max Power (Watts)"),
        blank=True,
        null=True)
    model = models.CharField(
        _("Model"),
        max_length=128)
    nominal_impedance = models.IntegerField(
        _("Nominal Impedance (Ohms)"),
        blank=True,
        null=True)
    resonant_frequency = models.FloatField(
        _("Resonant Frequency (Hertz)"),
        blank=True,
        null=True)
    rms_power = models.IntegerField(
        _("RMS power (Watts)"),
        blank=True,
        null=True)
    sensitivity = models.FloatField(
        _("Sensitivity (Decibels)"),
        blank=True,
        null=True)

    class Meta:
        ordering = ["model"]

    def __str__(self):
        return "{0} {1}".format(self.manufacturer.name, self.model)
