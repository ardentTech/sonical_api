from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .filters import DriverFilter
from .models import Driver, DriverGroup
from .serializers import DriverSerializer, DriverGroupSerializer


class DriverViewSet(mixins.ListModelMixin, GenericViewSet):

    filter_class = DriverFilter
    ordering_fields = ()
    queryset = Driver.objects.all()
    search_fields = ("model",)
    serializer_class = DriverSerializer


class DriverGroupViewSet(mixins.ListModelMixin, GenericViewSet):

    queryset = DriverGroup.objects.all()
    search_fields = ("name",)
    serializer_class = DriverGroupSerializer
