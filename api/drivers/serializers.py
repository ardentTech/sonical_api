from rest_framework import serializers

from .models import Driver, DriverGroup, DriverProductListing
from manufacturing.serializers import ManufacturerSerializer


class DriverProductListingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "created",
            "id",
            "modified",
            "path",
            "price",
        )
        model = DriverProductListing
        read_only_fields = ("created", "id", "modified",)


class DriverSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()
    driver_product_listings = DriverProductListingSerializer(many=True)

    class Meta:
        fields = (
            "bl_product",
            "created",
            "dc_resistance",
            "diaphragm_mass_including_airload",
            "electromagnetic_q",
            "id",
            "in_production",
            "frequency_response",
            "manufacturer",
            "max_power",
            "mechanical_q",
            "model",
            "modified",
            "nominal_diameter",
            "nominal_impedance",
            "driver_product_listings",
            "resonant_frequency",
            "rms_power",
            "sensitivity",
            "voice_coil_diameter",
            "voice_coil_inductance",
        )
        model = Driver
        read_only_fields = ("created", "id", "modified",)


class DriverGroupSerializer(serializers.ModelSerializer):

    drivers = DriverSerializer(allow_null=True, many=True, read_only=True)

    class Meta:
        fields = (
            "created",
            "drivers",
            "id",
            "modified",
            "name",
        )
        model = DriverGroup
        read_only_fields = ("created", "id", "modified",)
