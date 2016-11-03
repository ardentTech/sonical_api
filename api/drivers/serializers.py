from rest_framework import serializers

from .models import Driver
from manufacturing.serializers import ManufacturerSerializer


class DriverSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()

    class Meta:
        fields = (
            "created",
            "diameter",
            "id",
            "manufacturer",
            "max_power",
            "model",
            "modified",
            "nominal_impedance",
            "resonant_frequency",
            "rms_power",
            "sensitivity",)
        model = Driver
        read_only_fields = ("created", "id", "modified",)
