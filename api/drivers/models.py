from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from products.models import ProductListing
from utils.models import Creatable, Modifiable


class Driver(Creatable, Modifiable):

    bl_product = models.DecimalField(
        _("BL Product (Tm)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    compliance_equivalent_volume = models.DecimalField(
        _("Compliance Equivalent Volume (ft**3)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    basket_frame = models.ForeignKey(
        "manufacturing.Material",
        blank=True,
        null=True,
        related_name="driver_basket_frame",
        verbose_name=_("basket frame"))
    cone = models.ForeignKey(
        "manufacturing.Material",
        blank=True,
        null=True,
        related_name="driver_cone",
        verbose_name=_("cone"))
    cone_surface_area = models.DecimalField(
        _("Surface Area of Cone (cm**2)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    dc_resistance = models.DecimalField(
        _("DC Resistance (ohms)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    diaphragm_mass_including_airload = models.DecimalField(
        _("Diaphragm Mass Inc. Airload (g)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    electromagnetic_q = models.DecimalField(
        _("Electromagnetic Q"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    frequency_response = IntegerRangeField(
        _("Frequency Response (Hz)"),
        blank=True,
        null=True)
    in_production = models.BooleanField(
        _("In Production"),
        default=True)
    magnet = models.ForeignKey(
        "manufacturing.Material",
        blank=True,
        null=True,
        related_name="driver_magnet",
        verbose_name=_("magnet"))
    manufacturer = models.ForeignKey(
        "manufacturing.Manufacturer")
    max_power = models.IntegerField(
        _("Max Power (Watts)"),
        blank=True,
        null=True)
    max_linear_excursion = models.DecimalField(
        _("Maximum Linear Excursion (mm)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    mechanical_compliance_of_suspension = models.DecimalField(
        _("Mechanical Compliance of Suspension (mm/N)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    mechanical_q = models.DecimalField(
        _("Mechanical Q"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    model = models.CharField(
        _("Model"),
        db_index=True,
        max_length=128)
    nominal_diameter = models.DecimalField(
        _("Nominal Diameter (Inches)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    nominal_impedance = models.IntegerField(
        _("Nominal Impedance (Ohms)"),
        blank=True,
        null=True)
    resonant_frequency = models.DecimalField(
        _("Resonant Frequency (Hertz)"),
        blank=True,
        decimal_places=2,
        help_text="Fs",
        max_digits=7,
        null=True)
    rms_power = models.IntegerField(
        _("RMS power (Watts)"),
        blank=True,
        null=True)
    sensitivity = models.DecimalField(
        _("Sensitivity (Decibels)"),
        blank=True,
        decimal_places=2,
        help_text="2.83V/1m",
        max_digits=5,
        null=True)
    surround = models.ForeignKey(
        "manufacturing.Material",
        blank=True,
        null=True,
        related_name="driver_surround",
        verbose_name=_("surround"))
    voice_coil_diameter = models.DecimalField(
        _("Voice Coil Diameter (Inches)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    voice_coil_former = models.ForeignKey(
        "manufacturing.Material",
        blank=True,
        null=True,
        related_name="driver_voice_coil_former",
        verbose_name=_("voice coil former"))
    voice_coil_inductance = models.DecimalField(
        _("Voice Coil Inductance (MilliHenries)"),
        blank=True,
        decimal_places=2,
        max_digits=5,
        null=True)
    voice_coil_wire = models.ForeignKey(
        "manufacturing.Material",
        blank=True,
        null=True,
        related_name="driver_voice_coil_wire",
        verbose_name=_("voice coil wire"))

#    hifi_or_pa (application?)
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
#    slug?

    class Meta:
        ordering = ["model"]

    def __str__(self):
        return "{0} {1}".format(self.manufacturer.name, self.model)

    def total_q(self):
        return (
            (self.electromagnetic_q * self.mechanical_q) /
            (self.electromagnetic_q + self.mechanical_q))


class DriverGroup(Creatable, Modifiable):

    author = models.ForeignKey(
        "users.User",
        verbose_name=_("author"))
    drivers = models.ManyToManyField(
        "drivers.Driver", blank=True, verbose_name=_("drivers"))
    name = models.CharField(_("name"), max_length=128)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Driver Groups"

    def __str__(self):
        return "{0} {1}".format(self.id, self.name)


class DriverProductListing(ProductListing):

    driver = models.ForeignKey(
        "drivers.Driver",
        related_name="driver_product_listings",
        verbose_name=_("driver"))

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Driver Product Listings"

    def __str__(self):
        return "{0} {1}".format(self.dealer.name, self.driver.model)
