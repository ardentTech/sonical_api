from rest_framework import serializers

from .models import Manufacturer, Material


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "name",)
        model = Manufacturer
        read_only_fields = ("id",)


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("id", "name",)
        model = Material
        read_only_fields = ("id",)
