from rest_framework import serializers

from .models import Driver, DriverGroup, DriverProductListing
from manufacturing.serializers import ManufacturerSerializer, MaterialSerializer


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

    cone = MaterialSerializer()
    driver_product_listings = DriverProductListingSerializer(many=True)
    manufacturer = ManufacturerSerializer()
    surround = MaterialSerializer()
    voice_coil_former = MaterialSerializer()
    voice_coil_wire = MaterialSerializer()

    class Meta:
        fields = (
            "bl_product",
            "compliance_equivalent_volume",
            "cone",
            "cone_surface_area",
            "created",
            "dc_resistance",
            "diaphragm_mass_including_airload",
            "electromagnetic_q",
            "id",
            "in_production",
            "frequency_response",
            "manufacturer",
            "max_power",
            "maximum_linear_excursion",
            "mechanical_compliance_of_suspension",
            "mechanical_q",
            "model",
            "modified",
            "nominal_diameter",
            "nominal_impedance",
            "driver_product_listings",
            "resonant_frequency",
            "rms_power",
            "sensitivity",
            "surround",
            "voice_coil_diameter",
            "voice_coil_former",
            "voice_coil_inductance",
            "voice_coil_wire",
        )
        model = Driver
        read_only_fields = ("created", "id", "modified",)


class DriverGroupSerializer(serializers.ModelSerializer):

    drivers = DriverSerializer(allow_null=True, many=True, read_only=True)

    class Meta:
        fields = (
            "author",
            "created",
            "drivers",
            "id",
            "modified",
            "name",
        )
        model = DriverGroup
        read_only_fields = ("created", "id", "modified",)
