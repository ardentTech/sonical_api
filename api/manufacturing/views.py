from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Manufacturer, Material
from .serializers import ManufacturerSerializer, MaterialSerializer


class ManufacturerViewSet(mixins.ListModelMixin, GenericViewSet):

    queryset = Manufacturer.objects.all()
    search_fields = ("name",)
    serializer_class = ManufacturerSerializer


class MaterialViewSet(mixins.ListModelMixin, GenericViewSet):

    queryset = Material.objects.all()
    search_fields = ("name",)
    serializer_class = MaterialSerializer
