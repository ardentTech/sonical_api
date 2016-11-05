from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.models import Creatable, Modifiable


# @todo need concept of version?
class Driver(Creatable, Modifiable):

    nominal_diameter = models.FloatField(
        _("Nominal Diameter (Inches)"),
        blank=True,
        null=True)
    in_production = models.BooleanField(
        _("In Production"),
        default=True)
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
#    hifi_or_pa (application?)
#    frequency_response int -> int (Hz)
#    dc_resistance float (ohms)
#    voice_coil_inductance float (mH)
#    mechanical_q float
#    electromagnetic_q float
#    total_q float
#    compliance_equivalent_volume float (ft**3)
#    mechanical_compliance_of_suspension float (mm/N)
#    bl_product float (Tm)
#    diaphragm_mass float (g)
#    maximum_linear_excursion float (mm)
#    surface_area_of_cone float (cm**2)
#    cone_material
#    surround_material
#    voice_coil_wire_material
#    voice_coil_former
#    basket_frame_material
#    magnet_material
#    part_number
#    category
#    overall_outside_diameter
#    baffle_cutout_diameter
#    depth
#    bolt_circle_diameter
#    mounting_holes_count

    class Meta:
        ordering = ["model"]

    def __str__(self):
        return "{0} {1}".format(self.manufacturer.name, self.model)

    def validate_unique(self, exclude=None):
        # @todo validate model + manufacturer.name? part number?
        pass
