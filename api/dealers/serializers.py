from rest_framework import serializers

from .models import Dealer


class DealerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "created",
            "id",
            "modified",
            "name",
            "website",
        )
        model = Dealer
        read_only_fields = ("created", "id", "modified",)
