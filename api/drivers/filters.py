import django_filters

from .models import Driver


# @todo allow gt lt gte lte in addition to equality
class DriverFilter(django_filters.FilterSet):

    manufacturer = django_filters.CharFilter(name="manufacturer__name")

    class Meta:
        fields = [
            "dc_resistance",
            "in_production",
            "manufacturer",
            "max_power",
            "model",
            "nominal_diameter",
            "nominal_impedance",
            "resonant_frequency",
            "rms_power",
            "sensitivity",
        ]
        model = Driver
