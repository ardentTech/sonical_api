import django_filters

from .models import Driver
from utils.filter_fields import SonicalBooleanFilter


# @todo allow gt lt gte lte in addition to equality
class DriverFilter(django_filters.FilterSet):

    in_production = SonicalBooleanFilter()
    manufacturer = django_filters.CharFilter(name="manufacturer__name")

    class Meta:
        fields = [
            "dc_resistance",
            "electromagnetic_q",
            "in_production",
            "manufacturer",
            "max_power",
            "mechanical_q",
            "model",
            "nominal_diameter",
            "nominal_impedance",
            "resonant_frequency",
            "rms_power",
            "sensitivity",
            "voice_coil_inductance",
        ]
        model = Driver
