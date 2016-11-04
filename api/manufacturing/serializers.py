from rest_framework import serializers

from .models import Manufacturer, Material


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("created", "id", "modified", "name", "website",)
        model = Manufacturer
        read_only_fields = ("created", "id", "modified",)


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("created", "id", "modified", "name",)
        model = Material
        read_only_fields = ("created", "id", "modified",)
