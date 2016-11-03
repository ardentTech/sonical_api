from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Driver
from .serializers import DriverSerializer


class DriverViewSet(mixins.ListModelMixin, GenericViewSet):

    filter_class = None
    ordering_fields = ()
    queryset = Driver.objects.all()
    search_fields = ("model",)
    serializer_class = DriverSerializer
