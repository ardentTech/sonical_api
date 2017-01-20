from rest_framework import serializers


class IntegerRangeField(serializers.Field):
    """
    Returns data as a dict instead of a serialized dict.
    """

    def to_representation(self, obj):
        return {"lower": obj.lower, "upper": obj.upper}
