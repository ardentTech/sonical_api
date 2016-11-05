import django_filters

from .models import Driver


class DriverFilter(django_filters.FilterSet):

    manufacturer = django_filters.CharFilter(name="manufacturer__name")

    class Meta:
        fields = [
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
