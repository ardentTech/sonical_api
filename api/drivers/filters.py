import django_filters

from .models import Driver
from utils.filter_fields import SonicalBooleanFilter


# @todo re-add custom in_production filter
# @todo research 'icontains' for char fields
class DriverFilter(django_filters.FilterSet):

    in_production = SonicalBooleanFilter()

    class Meta:
        fields = {
            "dc_resistance": ["exact", "gt", "gte", "lt", "lte"],
            "electromagnetic_q": ["exact", "gt", "gte", "lt", "lte"],
            "manufacturer": ["exact"],
            "max_power": ["exact", "gt", "gte", "lt", "lte"],
            "mechanical_q": ["exact", "gt", "gte", "lt", "lte"],
            "model": ["contains"],
            "nominal_diameter": ["exact", "gt", "gte", "lt", "lte"],
            "nominal_impedance": ["exact", "gt", "gte", "lt", "lte"],
            "resonant_frequency": ["exact", "gt", "gte", "lt", "lte"],
            "rms_power": ["exact", "gt", "gte", "lt", "lte"],
            "sensitivity": ["exact", "gt", "gte", "lt", "lte"],
            "voice_coil_inductance": ["exact", "gt", "gte", "lt", "lte"],
        }
        model = Driver
