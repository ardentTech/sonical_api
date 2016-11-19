from rest_framework import serializers

from .models import Driver
from manufacturing.serializers import ManufacturerSerializer


class DriverSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()

    class Meta:
        fields = (
            "created",
            "dc_resistance",
            "electromagnetic_q",
            "id",
            "in_production",
            "manufacturer",
            "max_power",
            "mechanical_q",
            "model",
            "modified",
            "nominal_diameter",
            "nominal_impedance",
            "resonant_frequency",
            "rms_power",
            "sensitivity",
            "voice_coil_inductance",
        )
        model = Driver
        read_only_fields = ("created", "id", "modified",)
